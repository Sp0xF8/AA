import heapq

class formatter:
	RED = '\033[91m'
	GREEN = '\033[92m'
	BLUE = '\033[94m'
	YELLOW = '\033[93m'
	RESET = '\033[0m'
	BOLD = '\033[1m'
	ITALIC = '\033[3m'
	UNDERLINE = '\033[4m'

additional_routes = []

# Function to parse the csv file
def parse_csv(file_path):
	## read each entry in the csv file
	with open(file_path, 'r') as file:
		data = file.readlines()


	tuple_list = []
	## loop through each entry in the data
	for i in range(len(data)):
		### remove the newline character and split the data by the comma
		data[i] = data[i].strip().split(',')
		### convert the weight to an integer
		data[i][2] = int(data[i][2])
		### append the data to the tuple list
		tuple_list.append((data[i][0].strip().lower(), data[i][1].strip().lower(), data[i][2]))

	## return the tuple list
	return tuple_list

def add_route():
	print(formatter.RESET)
	print(formatter.BOLD + formatter.YELLOW + " "*30 + "/" + "-"*40 + "\\" + formatter.RESET)
	print(formatter.ITALIC + formatter.BLUE + " " * 36 + "Add a new route to the network")
	print(formatter.BOLD + formatter.YELLOW +  " "*30 + "\\" + "-"*40 + "/" + formatter.RESET)

	print(formatter.GREEN + "Please enter the following details to add a new route:\n")
	try:
		
		departure = input(formatter.BLUE +  " "*5 + "Enter the Departure station: " + formatter.GREEN + formatter.BOLD).strip().lower()
		destination = input(formatter.RESET + formatter.BLUE +  " "*5 + "Enter the Arrival station: " + formatter.GREEN + formatter.BOLD).strip().lower()
		weight_string = input(formatter.RESET + formatter.BLUE +  " "*5 + "Enter the cost of the route: " + formatter.GREEN + formatter.BOLD).strip()
	except KeyboardInterrupt:
		return

	while not weight_string.isdigit():
		print(formatter.RED + "\nInvalid input, please enter a valid number\n")
		weight_string = input(formatter.RESET + formatter.BLUE +  " "*5 + "Enter the cost of the route: " + formatter.GREEN + formatter.BOLD).strip()

	weight = int(weight_string)
	additional_routes.append((departure, destination, weight))

	print(formatter.RESET + formatter.GREEN + "\nRoute added successfully")
	try:
		input(formatter.RESET + formatter.GREEN + "Press enter to continue" + formatter.RESET)
	except KeyboardInterrupt:
		return

def combine_routes(edges):
	cmb = edges + additional_routes
	return cmb

def write_to_csv():
	data = combine_routes(parse_csv("task1_4_railway_network.csv"))
	with open("task1_4_railway_network.csv", 'w') as file:
		for dep, des, weight in data:
			file.write(f"{dep},{des},{weight}\n")

	print(formatter.GREEN + "Data written to file successfully" + formatter.RESET)
	try:
		input(formatter.GREEN + "Press enter to continue" + formatter.RESET)
	except KeyboardInterrupt:
		return

def print_stations(vertices):
	vertices.sort()

	print(formatter.RESET + formatter.BLUE + formatter.ITALIC)
	x = 0
	line = ""
	for vertex in vertices:
		
		for char in vertex.title():
			line += char

		length = len(vertex)
		total_boundary = 25
		remaining = total_boundary - length
		while remaining >= 0:
			line += " "
			remaining -= 1

		x += 1
		if (vertex == vertices[-1]) or (x % 4 == 0 and x != 0):
			print(line)
			line = ""
		
	print("\n" + formatter.RESET)
	# print(formatter.BLUE + " "*5 + vertex.capitalize())

def list_stations():
	vertices = get_vertices(fix_data(combine_routes(parse_csv("task1_4_railway_network.csv"))))
	##order the vertices in alphabetical order
	print(formatter.GREEN + "The stations in the network are:\n")
	print_stations(vertices)

	print(formatter.GREEN + "Total number of stations: " + formatter.BLUE + str(len(vertices)))
	try:
		input(formatter.RESET + formatter.GREEN + "Press enter to continue" + formatter.RESET)
	except KeyboardInterrupt:
		return

# Function to make the data bi-directional
def fix_data(data):
	
	tuple_list = []
	
	## loop through each entry in the data
	for i in range(len(data)):
		### create a new tuple with the destination and departure swapped
		new_tuple = (data[i][1], data[i][0], int(data[i][2]))
		### append the new tuple to the tuple list
		tuple_list.append(new_tuple)
		### append the original tuple to the tuple list
		tuple_list.append(data[i])
	## return the bi-directional tuple list
	return tuple_list

# Function to get the vertices from the edges
def get_vertices(edges):
	vertices = []
	## loop through each edge in the edges
	for i in range(len(edges)):
		### append the departure (which also includes the destination fix_data()) to the vertices list
		vertices.append(edges[i][0])
	## convert to a unique list
	vertices = list(set(vertices))
	## return the vertices
	return vertices

# function to find all shortest paths from departure and return the requested path
def dijkstra(start, end, edges, vertices):

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
			### pop the vertex with the smallest weight
			weight, current_vertex = heapq.heappop(min_heap)

			### if the current vertex is in the shortest paths, continue
			if current_vertex in shortest_paths:
				continue
			
			### update the weight to arrive at the current vertex
			shortest_paths[current_vertex] = weight


			for neighbour, neighbour_weight in adjacency_list[current_vertex]:
				if neighbour not in shortest_paths:
					heapq.heappush(min_heap, (weight + neighbour_weight, neighbour))
					
					previous_vertices[neighbour] = current_vertex

		# Reconstructing the shortest path
		path = []
		current = end
		while current != start:
			path.append(current)
			current = previous_vertices[current]
		path.append(start)
		path.reverse()

		return path, shortest_paths[end]
	except KeyError:
		print(formatter.RED + "No path found between the stations" + formatter.RESET)
		return None, None

def validate_staton(station , stations):
	## check if the station is a substring of any of the stations in the network and return a list of stations which match

	stations =  get_vertices(fix_data(combine_routes(parse_csv("task1_4_railway_network.csv"))))

	for stat in stations:
		if station == stat:
			return True

	stat_matches = []
	print(formatter.RED + f"\nStation {station} not found in the network, did you possibly mean:" + formatter.RESET)
	for stat in stations:
		if station in stat:
			stat_matches.append(stat)
	
	print_stations(stat_matches)
	print("\n")
	return False

def find_shortest_path():

	print(formatter.RESET)
	print(formatter.BOLD + formatter.YELLOW + " "*25 + "/" + "-"*50 + "\\" + formatter.RESET)
	print(formatter.ITALIC + formatter.BLUE + " " * 22 + "Search for the path between two stations with minimum cost")
	print(formatter.BOLD + formatter.YELLOW +  " "*25 + "\\" + "-"*50 + "/")
	print(formatter.RESET)

	edges = fix_data(combine_routes(parse_csv("task1_4_railway_network.csv")))
	vertices = get_vertices(edges)
	try:

		while True:
			departure = input(formatter.BLUE  +  " "*5 +  "Enter the departure station: " + formatter.GREEN + formatter.BOLD).strip().lower()
			if validate_staton(departure, vertices):
				print(formatter.RESET + formatter.GREEN + "Station " + formatter.YELLOW + departure.title() + formatter.GREEN + " found in the network" + formatter.RESET)
				break

		while True:
			destination = input(formatter.RESET + formatter.BLUE  +  " "*5 +  "Enter the arrival station: " + formatter.GREEN + formatter.BOLD).strip().lower()
			if validate_staton(destination, vertices):
				print(formatter.RESET + formatter.GREEN + "Station " + formatter.YELLOW + destination.title() + formatter.GREEN + " found in the network" + formatter.RESET)
				break

		path, shortest_path = dijkstra(departure, destination, edges, vertices)

		if path is None and shortest_path is None:
			input(formatter.RESET + formatter.RED + "Press enter to continue" + formatter.RESET)
			return

		print(formatter.GREEN + "The total cost is " + formatter.YELLOW + formatter.BOLD + str(shortest_path) + formatter.RESET + formatter.GREEN + " with the following route " + formatter.YELLOW + formatter.BOLD + str(path) + formatter.RESET)
		input(formatter.RESET + formatter.GREEN + "Press enter to continue" + formatter.RESET)

	except KeyboardInterrupt:
		return

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

		try:
			option = input(formatter.GREEN + "Enter your option: " + formatter.BOLD)
		except KeyboardInterrupt:
			break
		print(formatter.ITALIC + formatter.YELLOW + "~"*100 + formatter.RESET)
		print(formatter.YELLOW + " "*30 + "\\" + "-"*40 + "/" + formatter.RESET)
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