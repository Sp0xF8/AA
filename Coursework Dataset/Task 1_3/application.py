import multiprocessing as mp
import os, sys

def get_Ram():
	proc = os.popen('wmic memorychip get capacity')
	ram = proc.readlines()
	proc.close()


	## for each line in the output
	total_ram = 0

	for each in ram:
		split = each.split(" ")
		## for each word in the line
		for word in split:
			## if the word is a number
			if word.isdigit():
				## add it to the total
				total_ram += int(word)

	## convert to GB from bytes
	total_ram = total_ram / (1024**3)

	return total_ram

def check_capacity():
	# print number of processors
	if mp.cpu_count() < 4:
		# print("Number of processors is less than 4")
		n = 2
	elif mp.cpu_count() < 8:
		# print("Number of processors is less than 8")
		n = 4
	else:
		# print("Number of processors is greater than 8")
		n = 6
	
	return n# 4


def get_params(path, verbose, force=None):

	ram = get_Ram()
	n = check_capacity()

	

	size = 0
	available_ram = ram * 0.4

	with open(path, "r", encoding='utf8') as f:
		text = f.read()

	size = sys.getsizeof(text)
	# convert to GB
	size = size / (1024**3)
	length = len(text)

	if verbose:
		print("Total RAM: ", ram)
		print("Aproximated RAM: ", available_ram)
		print("Number of processors to be used: ", n)
		print("Size of file: ", size)
		print("Length of file: ", length)
	div = 1

	if (size * n > available_ram /2) or (force == 1 or force == 2): 
		div = n
		
		size = size / n
		length = int(length / n)

		if (size * n > available_ram /2) or (force == 2):
			div = n*n
			size = size / n 
			length = int(length / n)

	else:
		print("Size of file * number of processors is less than available RAM")
		print("The file will not be split into smaller parts")

	if verbose:
		print("Number of parts: ", div)
		print("Size of each part: ", size)
		print("Length of each part: ", length)
		input("Press Enter to continue...")

	return length, text, div

def get_patterns(path):
	patterns = []
	with open(path, "r", encoding='utf8') as f:
		for line in f:
			patterns.append(line.strip())

	print(patterns)
	return patterns

def search(pattern, text, result_queue):
	count = 0
	for i in range(len(text) - len(pattern) + 1):
		if text[i] == pattern[0]:
			found = True
			for j in range(1, len(pattern)):
				if text[i + j] != pattern[j]:
					found = False
					i += j
					break
			if found:
				count += 1
	result_queue.put((pattern, count))

def check_patterns(text_path, patterns_path, verbose=False, force=None):

	n = check_capacity()

	result_queue = mp.Queue()
	name_counts = {}

	length, text, div = get_params(text_path, verbose, force)
	patterns = get_patterns(patterns_path)


	if div != 1:

		x = 0
		while x < len(patterns):
			loop = 0
			pos = 0
			end = length
			pattern = patterns[x]
			pattern_length = len(pattern)

			if verbose:
				print("Pattern: ", pattern)
			while pos < len(text):
				processes = []
				if end == len(text):
					break
				

				l_start = loop +1

				for i in range(n):
					loop += 1
					start = pos - int(pattern_length/2)
					if start < 0:
						start = 0

					end = pos + length + int(pattern_length/2)
					if end > len(text):
						end = len(text)
					if verbose:
						# print("Start: ", start)
						# print("End: ", end)
						print("Qeueing: ", pattern, " Part: ", loop)
					process = mp.Process(target=search, args=(pattern, text[start:end], result_queue))
					processes.append(process)

					if end == len(text):
						if verbose:
							print("End of text reached")
						break

					pos += length

				
				for process in processes:
					process.start()

				for process in processes:
					process.join()

				while not result_queue.empty():
					pattern, count = result_queue.get()
					if pattern not in name_counts:
						name_counts[pattern] = 0
					name_counts[pattern] += count
					if verbose:
						print("Received: ", pattern, " Count: ", count, " Part: ", l_start)
					l_start += 1
				if verbose:
					print("Total for: ", pattern, " is: ", name_counts[pattern])
			x += 1

		return name_counts
	else:
		x = 0
		while x < len(patterns):
			processes = []

			if n > (len(patterns) - x):
				stop = len(patterns)
			else:
				stop = x + n

			for i in range(x, stop):
				pattern = patterns[i]
				print("Qeueing: ", pattern)
				process = mp.Process(target=search, args=(pattern, text, result_queue))
				processes.append(process)

			for process in processes:
				process.start()

			for process in processes:
				process.join()

			while not result_queue.empty():
				pattern, count = result_queue.get()
				name_counts[pattern] = count
				print("Received: ", pattern, " Count: ", count)
			x += n
		return name_counts

if __name__ == '__main__':

	# search_base_length, text, div = search_size("task1_3_text.txt")
	# print("Base Length: ", search_base_length)

	name_counts = check_patterns("task1_3_text.txt", "task1_3_names.txt", verbose=True, force=2)
	l_counts = list(name_counts.items())
	str_counts =str(l_counts)

	#remove brackets
	str_counts = str_counts.replace("[", "")
	str_counts = str_counts.replace("]", "")

	print(str_counts)

	with open("task1_3_output.txt", "w", encoding='utf8') as f:
		f.write(str_counts)


#output
##('Harry', 3991), ('Ron', 1185), ('Hermione', 1217), ('Hagrid', 168), ('Dumbledore', 588), ('Draco', 62), ('McGonagall', 70), ('Snape', 292), ('Gilderoy', 0), ('Ginny', 122), ('Malfoy', 89), ('Vernon', 50), ('Arthur', 20), ('Molly', 11), ('Sirius', 69), ('Remus', 21), ('Peter', 2), ('Neville', 89), ('Fred', 94), ('George', 77), ('Moody', 30), ('Cho', 13), ('Voldemort', 446), ('Bellatrix', 98), ('Luna', 140)

##expected output
##('Harry', 3991), ('Ron', 1185), ('Hermione', 1217), ('Hagrid', 168), ('Dumbledore', 588), ('Draco', 62), ('McGonagall', 70), ('Snape', 292), ('Gilderoy', 0), ('Ginny', 122), ('Malfoy', 89), ('Vernon', 50), ('Arthur', 20), ('Molly', 11), ('Sirius', 69), ('Remus', 21), ('Peter', 2), ('Neville', 89), ('Fred', 94), ('George', 77), ('Moody', 30), ('Cho', 13), ('Voldemort', 446), ('Bellatrix', 98), ('Luna', 140)