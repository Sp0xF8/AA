import heapq


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
		tuple_list.append((data[i][0].lower(), data[i][1].lower(), data[i][2]))

	## return the tuple list
	return tuple_list

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




edges = parse_csv("task1_4_railway_network.csv")
edges = fix_data(edges)



departure = input("Enter the departure station: ")
destination = input("Enter the arrival station: ")

departure = departure.lower()
destination = destination.lower()

vertices = get_vertices(edges)


path, shortest_path = dijkstra(departure, destination, edges, vertices)

print(f"The total cost is {shortest_path} with the following route {path}")

