import heapq

def parse_csv(file_path):
	with open(file_path, 'r') as file:
		data = file.readlines()

	tuple_list = []
		
	for i in range(len(data)):
		data[i] = data[i].strip().split(',')
		data[i][2] = int(data[i][2])
		tuple_list.append((data[i][0].capitalize(), data[i][1].capitalize(), data[i][2]))


	return tuple_list

def fix_data(data):
	
	tuple_list = []
	
	for i in range(len(data)):
		new_tuple = (data[i][1], data[i][0], int(data[i][2]))
		tuple_list.append(new_tuple)
		tuple_list.append(data[i])



	return tuple_list


def get_vertices(data):
	vertices = []
	for i in range(len(data)):
		vertices.append(data[i][0])
		vertices.append(data[i][1])

	vertices = list(set(vertices))
	return vertices



def dijkstra(start, end, edges, vertices):


	adjacency_list = {}
	for i in vertices:
		adjacency_list[i] = []

	# print(edges)
	for dep, des, weight in edges:
		print(dep, des, weight)
		adjacency_list[dep].append((des, weight))

	shortest_path = {}
	min_heap = [(0, start)]

	while min_heap:
		weight, current_vertex = heapq.heappop(min_heap)

		if current_vertex in shortest_path:
			continue

		shortest_path[current_vertex] = weight

		for neighbour, neighbour_weight in adjacency_list[current_vertex]:
			if neighbour not in shortest_path:
				heapq.heappush(min_heap, (weight + neighbour_weight, neighbour))

	
	for vertex in vertices:
		if vertex not in shortest_path:
			shortest_path[vertex] = float('inf')

	return shortest_path


	
	

def main():
    
	
	edges = parse_csv("task1_4_railway_network.csv")
	edges = fix_data(edges)
	# print(data)


	# departure = input("Enter the departure station: ")
	# arrival = input("Enter the arrival station: ")
	departure = "BRISTOL TEMPLE MEADS"
	destination = "London"

	destination = destination.capitalize()
	departure = departure.capitalize()

	vertices = get_vertices(edges)

	print(edges)


	
	shortest_path = dijkstra(departure, destination, edges, vertices)
	print(shortest_path)



if __name__ == "__main__":
	main()