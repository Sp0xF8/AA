import heapq


## Class to format the output for increased user experience
class formatter:
	RED = '\033[91m'
	GREEN = '\033[92m'
	BLUE = '\033[94m'
	YELLOW = '\033[93m'
	RESET = '\033[0m'
	BOLD = '\033[1m'
	ITALIC = '\033[3m'
	UNDERLINE = '\033[4m'

## Global variable to store the new routes added by the user
additional_routes = []

# Function to parse the csv file
def parse_csv(file_path):
	## read each entry in the csv file
	with open(file_path, 'r') as file:
		data = file.readlines()


	tuple_list = []
	## loop through each entry in the data
	for i in range(len(data)):
		## remove the newline character and split the data by the comma
		data[i] = data[i].strip().split(',')
		## convert the weight to an integer
		data[i][2] = int(data[i][2])
		## append the data to the tuple list, stripping tailing spaces and converting to lowercase
		tuple_list.append((data[i][0].strip().lower(), data[i][1].strip().lower(), data[i][2]))

	## return the tuple list
	return tuple_list

## function to add a new route to the network
def add_route():
	print(formatter.RESET)
	print(formatter.BOLD + formatter.YELLOW + " "*30 + "/" + "-"*40 + "\\" + formatter.RESET)
	print(formatter.ITALIC + formatter.BLUE + " " * 36 + "Add a new route to the network")
	print(formatter.BOLD + formatter.YELLOW +  " "*30 + "\\" + "-"*40 + "/" + formatter.RESET)

	print(formatter.GREEN + "Please enter the following details to add a new route:\n")

	## wrapped in a try except block to handle keyboard interrupts as a way to exit the function
	try:
		## get the departure, destination and weight from the user - strip and lower to match the format of the data
		departure = input(formatter.BLUE +  " "*5 + "Enter the Departure station: " + formatter.GREEN + formatter.BOLD).strip().lower()
		destination = input(formatter.RESET + formatter.BLUE +  " "*5 + "Enter the Arrival station: " + formatter.GREEN + formatter.BOLD).strip().lower()
		weight_string = input(formatter.RESET + formatter.BLUE +  " "*5 + "Enter the cost of the route: " + formatter.GREEN + formatter.BOLD).strip()

		## validate the weight input as a number
		while not weight_string.isdigit():
			print(formatter.RED + "\nInvalid input, please enter a valid number\n")
			## strip to remove leading and trailing spaces including the newline character
			weight_string = input(formatter.RESET + formatter.BLUE +  " "*5 + "Enter the cost of the route: " + formatter.GREEN + formatter.BOLD).strip()
	except KeyboardInterrupt:
		return

	## convert the weight to an integer
	weight = int(weight_string)
	## append the new route to the additional routes list
	additional_routes.append((departure, destination, weight))

	print(formatter.RESET + formatter.GREEN + "\nRoute added successfully")
	## wrapped in a try except block to handle keyboard interrupts as a way to exit the function
	try:
		## prompt the user to press enter to continue
		input(formatter.RESET + formatter.GREEN + "Press enter to continue" + formatter.RESET)
	except KeyboardInterrupt:
		return

## quality of life function to combine the routes and the additional routes
def combine_routes(edges):
	cmb = edges + additional_routes
	return cmb

## function to write the new routes to the csv file
def write_to_csv():
	## combine the origonal routes and the additional routes
	data = combine_routes(parse_csv("task1_4_railway_network.csv"))
	## open the file in write mode
	with open("task1_4_railway_network.csv", 'w') as file:
		## loop through each tuple in the data
		for dep, des, weight in data:
			## write the data to the file in the format of departure, destination, weight
			file.write(f"{dep},{des},{weight}\n")

	print(formatter.GREEN + "Data written to file successfully" + formatter.RESET)

	## wrapped in a try except block to handle keyboard interrupts as a way to exit the function
	try:
		input(formatter.GREEN + "Press enter to continue" + formatter.RESET)
	except KeyboardInterrupt:
		return

## function to print the stations in the network in 4 columns of 25 characters
def print_stations(vertices):
	## sort the vertices in alphabetical order
	vertices.sort()

	print(formatter.RESET + formatter.BLUE + formatter.ITALIC)
	
	## declare variables to keep track of the number of columns which have been built
	x = 0
	## declare a variable to store the line to be printed
	line = ""
	## loop through each vertex in the vertices
	for vertex in vertices:

		## loop through each character in the vertex
		for char in vertex.title():
			## append the character to the line
			line += char
		## calculate the remaining spaces to fill the 25 character length
		length = len(vertex)
		total_boundary = 25
		remaining = total_boundary - length

		## fill the remaining spaces with spaces
		line += " " * remaining
		## increment the number of columns built
		x += 1

		## if the last station has been reached or the number of columns built is a multiple of 4 and not 0
		if (vertex == vertices[-1]) or (x % 4 == 0 and x != 0):
			## print the line
			print(line)
			## reset the line
			line = ""
		
	print("\n" + formatter.RESET)
	# print(formatter.BLUE + " "*5 + vertex.capitalize())

## function to list all the stations in the network
def list_stations():

	## get the vertices from the routes in the existing csv file and the additional routes
	vertices = get_vertices(fix_data(combine_routes(parse_csv("task1_4_railway_network.csv"))))
	##order the vertices in alphabetical order
	print(formatter.GREEN + "The stations in the network are:\n")
	print_stations(vertices)

	print(formatter.GREEN + "Total number of stations: " + formatter.BLUE + str(len(vertices)))

	## wrapped in a try except block to handle keyboard interrupts as a way to exit the function
	try:
		input(formatter.RESET + formatter.GREEN + "Press enter to continue" + formatter.RESET)
	except KeyboardInterrupt:
		return

## function to make the data bi-directional
def fix_data(data):
	
	## create an empty list to store the bi-directional tuples
	tuple_list = []
	
	## loop through each entry in the data
	for i in range(len(data)):
		## create a new tuple with the destination and departure swapped
		new_tuple = (data[i][1], data[i][0], int(data[i][2]))
		## append the new tuple to the tuple list
		tuple_list.append(new_tuple)
		## append the original tuple to the tuple list
		tuple_list.append(data[i])
	## return the bi-directional tuple list
	return tuple_list

## function to get the vertices from the edges
def get_vertices(edges):
	## create an empty list to store the vertices
	vertices = []
	## loop through each edge in the edges
	for i in range(len(edges)):
		## append the departure (which also includes the destination fix_data()) to the vertices list
		vertices.append(edges[i][0])
	## convert to a unique list
	vertices = list(set(vertices))
	## return the vertices
	return vertices

# function to find all shortest paths from departure and return the requested path
def dijkstra(start, end, edges, vertices):

	## wrapped in a try except block to handle key errors when the path is not found
	try:
		## create an adjacency list for the vertices and their neighbours
		adjacency_list = {}
		## loop through each vertex in the vertices
		for i in vertices:
			### set the adjacency list for the vertex to an empty list
			adjacency_list[i] = []

		## loop through each tuple in the edges list
		for dep, des, weight in edges:
			### append the destination and weight to the adjacency list for the departure
			adjacency_list[dep].append((des, weight))

		## create shortest paths dictionary
		shortest_paths = {}
		## create a min heap
		min_heap = [(0, start)]
		## create a previous vertices dictionary
		previous_vertices = {}

		## loop while the min heap is not empty
		while min_heap:
			## pop the vertex with the smallest weight
			weight, current_vertex = heapq.heappop(min_heap)

			## if the current vertex is in the shortest paths, continue
			if current_vertex in shortest_paths:
				continue
			
			## update the weight to arrive at the current vertex
			shortest_paths[current_vertex] = weight

			## for each tuple in the adjacency list for the current vertex
			for neighbour, neighbour_weight in adjacency_list[current_vertex]:
				## if the neighbour is not in the shortest paths
				if neighbour not in shortest_paths:
					## push the neighbour and the weight to the min heap
					heapq.heappush(min_heap, (weight + neighbour_weight, neighbour))
					
					## update with the previous vertex
					previous_vertices[neighbour] = current_vertex

		## Reconstructing the shortest path
		path = []
		## set the current vertex to the end
		current = end
		while current != start:
			path.append(current)
			current = previous_vertices[current]

		## append the start to the path
		path.append(start)
		## reverse the path to get the correct order
		path.reverse()
		return path, shortest_paths[end]
	
	except KeyError:
		print(formatter.RED + "No path found between the stations" + formatter.RESET)
		return None, None

## function to validate the station input when finding tickets
def validate_staton(station , stations):
	
	## get a list of all the stations in the network
	stations =  get_vertices(fix_data(combine_routes(parse_csv("task1_4_railway_network.csv"))))

	## loop through each station in the network
	for stat in stations:
		## if the station is found in the network as a direct match, return true
		if station == stat:
			return True
	## at this point, the station is not found in the network
	## create an empty list to store the stations that match the input
	stat_matches = []
	print(formatter.RED + f"\nStation {station} not found in the network, did you possibly mean:" + formatter.RESET)

	## loop through each station in the network
	for stat in stations:
		## check if the input is a substring of the station
		if station in stat:
			## append the station to the matches list
			stat_matches.append(stat)
	
	## print the stations that match the input
	if stat_matches:
		print_stations(stat_matches)
	print("\n")
	return False

## function to find the shortest path between two stations with minimum cost
def find_shortest_path():

	print(formatter.RESET)
	print(formatter.BOLD + formatter.YELLOW + " "*25 + "/" + "-"*50 + "\\" + formatter.RESET)
	print(formatter.ITALIC + formatter.BLUE + " " * 22 + "Search for the path between two stations with minimum cost")
	print(formatter.BOLD + formatter.YELLOW +  " "*25 + "\\" + "-"*50 + "/")
	print(formatter.RESET)

	## get the bi-directional edges from the csv file and the additional routes
	edges = fix_data(combine_routes(parse_csv("task1_4_railway_network.csv")))
	## get the vertices from the edges
	vertices = get_vertices(edges)

	## wrapped in a try except block to handle keyboard interrupts as a way to exit the function
	try:

		## validate the departure station
		while True:
			## strip and lower the input to match the format of the data
			departure = input(formatter.BLUE  +  " "*5 +  "Enter the departure station: " + formatter.GREEN + formatter.BOLD).strip().lower()
			if validate_staton(departure, vertices):
				print(formatter.RESET + formatter.GREEN + "Station " + formatter.YELLOW + departure.title() + formatter.GREEN + " found in the network" + formatter.RESET)
				break
		## validate the destination station
		while True:
			## strip and lower the input to match the format of the data
			destination = input(formatter.RESET + formatter.BLUE  +  " "*5 +  "Enter the arrival station: " + formatter.GREEN + formatter.BOLD).strip().lower()
			if validate_staton(destination, vertices):
				print(formatter.RESET + formatter.GREEN + "Station " + formatter.YELLOW + destination.title() + formatter.GREEN + " found in the network" + formatter.RESET)
				break
		
		## find the shortest path and the price between the departure and destination
		path, path_price = dijkstra(departure, destination, edges, vertices)

		if path is None and path_price is None:
			input(formatter.RESET + formatter.RED + "Press enter to continue" + formatter.RESET)
			return

		## print the path and price in the format requested
		print(formatter.GREEN + "The total cost is " + formatter.YELLOW + formatter.BOLD + str(path_price) + formatter.RESET + formatter.GREEN + " with the following route " + formatter.YELLOW + formatter.BOLD + str(path) + formatter.RESET)
		input(formatter.RESET + formatter.GREEN + "Press enter to continue" + formatter.RESET)

	except KeyboardInterrupt:
		return


## function to continuously display the menu
def menu():
	while True:
		print(formatter.RESET + "\n")
		print(formatter.BOLD + formatter.YELLOW + " "*30 + "/" + "-"*39 + "\\" + formatter.RESET)
		print(formatter.BOLD + formatter.ITALIC + formatter.YELLOW + "="*100 + formatter.RESET)
		print(formatter.BLUE +" "*30 + "Welcome to the Horizion Rails application")
		print(formatter.BOLD + formatter.ITALIC + formatter.YELLOW + "~"*100 + formatter.RESET)
		print(formatter.BOLD + formatter.YELLOW + " "*30 + "\\" + "-"*39 + "/" + formatter.RESET)
		print(formatter.GREEN + "Please select an option\n")
		print(formatter.BLUE +" "*5 + "1. Add a new tempoary Route to the network")
		print(" "*5 + "2. Find the shortest path between two stations with a Minimum cost")
		print(" "*5 + "3. List all the stations in the network")
		print(" "*5 + "4. Save the new routes to the network")
		print(" "*5 + "5. Exit \n")

		## wrapped in a try except block to handle keyboard interrupts as a way to exit the function
		try:
			option = input(formatter.GREEN + "Enter your option: " + formatter.BOLD)
		except KeyboardInterrupt:
			break
		print(formatter.ITALIC + formatter.YELLOW + "~"*100 + formatter.RESET)
		print(formatter.YELLOW + " "*30 + "\\" + "-"*40 + "/" + formatter.RESET)

		## python version of switch statement to handle the user input for the menu
		if option == '1':
			add_route()
		elif option == '2':
			find_shortest_path()
		elif option == '3':
			list_stations()
		elif option == '4':
			write_to_csv()
		elif option == '5':
			break
		else:
			print(formatter.RED + f"Invalid option, {option}, please try again" + formatter.RESET)

	print(formatter.GREEN + "\nExiting the application, thank you for choosing Horizon Rails" + formatter.RESET)



if __name__ == "__main__":
	menu()