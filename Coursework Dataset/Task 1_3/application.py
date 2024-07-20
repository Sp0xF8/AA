import multiprocessing as mp
import os, sys


## get the total RAM of the system
def get_Ram(verbose):
	## open a process with the Windows Management Instrumentation Command-line (WMIC) to get the size of the memory chips
	proc = os.popen('wmic memorychip get capacity')
	## read the output
	ram = proc.readlines()
	## close the process
	proc.close()

	if verbose:
		print("Entire RAM lookup:")
		print(ram)

	total_ram = 0

	## for each line in the output
	for each in ram:
		## split the line by spaces
		split = each.split(" ")
		## for each word in the line
		for word in split:
			## if the word is a number, it is the size of a memory chip
			if word.isdigit():
				## add byte size of the chip to the total RAM
				total_ram += int(word)

	## convert to GB from bytes
	total_ram = total_ram / (1024**3)

	return total_ram

## get the number of processes that can be used whilst maintaining system performance
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

## get the approximate size of the file to ensure it can be processed without exceeding the available RAM
def get_params(path, verbose, force=None):

	## get the total RAM of the system
	ram = get_Ram(verbose)
	## get the number of processors that can be used whilst maintaining system performance
	n = check_capacity()
	## assume the available RAM is 40% of the total RAM
	available_ram = ram * 0.4

	with open(path, "r", encoding='utf8') as f:
		text = f.read()

	## get the size of the file in bytes
	size = 0
	size = sys.getsizeof(text)
	## convert to GB
	size = size / (1024**3)
	## get the length of the file
	length = len(text)

	if verbose:
		print("Total RAM: ", ram)
		print("Aproximated RAM: ", available_ram)
		print("Number of processors to be used: ", n)
		print("Size of file: ", size)
		print("Length of file: ", length)
	
	## define the number of parts the file will be split into
	div = 1

	## if the system is not capable of processing the whole file n times with half the available RAM
	if (size * n > available_ram /2) or (force == 1 or force == 2): 
		## split the file into n parts
		div = n
		## get the size of each part
		size = size / div
		## get the length of each part
		length = int(length / div)

		## if the system is not able to process the whole file in n parts with half the available RAM
		if (size * n > available_ram /2) or (force == 2):
			## split the file into n^2 parts, (each previously defined part into n parts)
			div = n*n
			## get the size of each part
			size = size / n 
			## get the length of each part
			length = int(length / n)

	## if the system is able to process the whole file n times with half the available RAM
	else:
		print("Size of file * number of processors is less than available RAM")
		print("The file will not be split into smaller parts")

	if verbose:
		print("Number of parts: ", div)
		print("Size of each part: ", size)
		print("Length of each part: ", length)
		input("Press Enter to continue...")

	return length, text, div

## get the patterns to be searched for
def get_patterns(path):
	## define the list to store the patterns
	patterns = []
	## open the file containing the patterns
	with open(path, "r", encoding='utf8') as f:
		## for each line in the file
		for line in f:
			## add the line to the list of patterns after removing redundant characters
			patterns.append(line.strip())

	print(patterns)
	return patterns

## calculate the Longest Prefix Suffix (LPS) array for the pattern
def calc_lps(pattern):
	## get the length of the pattern
	pattern_length = len(pattern)
	## define the LPS array
	lps = [0] * pattern_length

	## define the index variables
	i = 0
	j = 1

	## loop through the pattern
	while lps[pattern_length - 1] == None:
		## if the characters at the current indexes are the same
		if pattern[i] == pattern[j]:
			
			## set the value of the LPS array at the current index to the value of i + 1
			lps[j] = i + 1
			## increment the index variables
			i += 1
			j += 1
		## if the characters are not the same
		else:
			## if it is the first character
			if i == 0:
				## set the value of the LPS array at the current index to 0
				lps[j] = 0
				## increment the index variable
				j += 1
			## if it is not the first character
			else:
				## set the value of i to the value of the LPS array at the previous index
				i = lps[i - 1]
	
	## return the LPS array
	return lps

## the Knuth-Morris-Pratt (KMP) algorithm to search for the pattern in the text
def kmp(pattern, text, result_queue):
	## define the count variable
	count = 0
	## get the length of the pattern and the text
	pattern_length = len(pattern)
	text_length = len(text)

	## calculate the LPS array for the pattern
	lps = calc_lps(pattern)

	## define the index variables
	i = 0
	j = 0

	## itterate through the text until the end is reached
	while i < text_length:
		## if the characters at the current indexed values of both the pattern and the text are the same
		if pattern[j] == text[i]:
			## increment the index variables
			i += 1
			j += 1

			## if the index variable is equal to the length of the pattern
			if j == pattern_length:
				## pattern found - increment the count
				count += 1
				## set the index variable to the value of the LPS array at the previous index
				j = lps[j - 1]

		## if the characters are not the same
		else:
			## if it is the first character of the pattern
			if j == 0:
				## increment the index variable
				i += 1
			## if it is not the first character of the pattern
			else:
				## set the index variable to the value of the LPS array at the previous index
				j = lps[j - 1]

	## add the pattern and the count to the result queue (memory) shared with the main process
	result_queue.put((pattern, count))


## check the patterns in the text while maintaining system performance
def check_patterns(text_path, patterns_path, verbose=False, force=None):

	## get the number of processors that can be used 
	n = check_capacity()

	## define the result queue (shared memory) to store the results of the processes
	result_queue = mp.Queue()
	## define the dictionary to store the counts of the patterns
	name_counts = {}

	## get the paramaters necessary to process the text without exceeding the available RAM
	length, text, div = get_params(text_path, verbose, force)
	## get the patterns to be searched for
	patterns = get_patterns(patterns_path)

	## if the file is split into parts
	if div != 1:

		## define the index variable
		x = 0
		## loop through the patterns
		while x < len(patterns):
			## define the index variables
			loop = 0
			pos = 0
			end = length

			## get the current pattern to be searched for and its length
			pattern = patterns[x]
			pattern_length = len(pattern)
			
			if verbose:
				print("Pattern: ", pattern)

			## loop until the end of the text is reached
			while pos < len(text):
				## define the list to store the processes
				processes = []
				## if the end of the text is reached
				if end == len(text):
					break
				
				## define the index variable
				l_start = loop +1
				## loop through the parts of the text
				for i in range(n):
					loop += 1
					## calculate the start pos to ensure a pattern occurance is not split between parts
					start = pos - int(pattern_length/2)

					## if the start of the part is less than 0
					if start < 0:
						## set the start to 0
						start = 0
					## calculate the end pos to ensure a pattern occurance is not split between parts
					end = pos + length + int(pattern_length/2)
					if end > len(text):
						end = len(text)
					if verbose:
						# print("Start: ", start)
						# print("End: ", end)
						print("Qeueing: ", pattern, " Part: ", loop)

					## define a process to search for the pattern in the part of the text
					process = mp.Process(target=kmp, args=(pattern, text[start:end], result_queue))
					## add the process to the list of processes
					processes.append(process)

					if end == len(text):
						if verbose:
							print("End of text reached")
						break
					## increment the position variable
					pos += length

				## start the processes
				for process in processes:
					process.start()

				## wait for the processes to finish
				for process in processes:
					process.join()

				## loop through the results in the result queue (shared memory)
				while not result_queue.empty():
					## get the pattern and the count from the result queue
					pattern, count = result_queue.get()
					## if the pattern is not in the dictionary, add it
					if pattern not in name_counts:
						name_counts[pattern] = 0
					## increment the count of the pattern
					name_counts[pattern] += count
					if verbose:
						print("Received: ", pattern, " Count: ", count, " Part: ", l_start)
					## increment the index variable for the parts
					l_start += 1
				if verbose:
					print("Total for: ", pattern, " is: ", name_counts[pattern])

			## increment the index variable for the patterns
			x += 1

		return name_counts
	
	## if the file is not split into parts
	else:
		## define the index variable to loop through the patterns
		x = 0
		## loop through the patterns
		while x < len(patterns):
			## define the list to store the processes
			processes = []

			## calculate the number of patterns to be searched for in this iteration
			## if the number of remaining patterns is less than the number of processors
			if n > (len(patterns) - x):
				## the stop index is the length of the patterns
				stop = len(patterns)
			## if the number of remaining patterns is greater than the number of processors
			else:
				## the stop index is the current index plus the number of processors available
				stop = x + n

			## loop through the patterns to be searched for in this iteration
			for i in range(x, stop):
				## get the current pattern to be searched for
				pattern = patterns[i]
				print("Qeueing: ", pattern)
				## define a process to search for the pattern in the text
				process = mp.Process(target=kmp, args=(pattern, text, result_queue))
				## add the process to the list of processes
				processes.append(process)

			## start the processes
			for process in processes:
				process.start()

			## wait for the processes to finish
			for process in processes:
				process.join()

			## loop through the results in the result queue (shared memory)
			while not result_queue.empty():
				## get a pattern and the count from the result queue and remove it from the queue
				pattern, count = result_queue.get()
				## add the pattern and the count to the dictionary
				name_counts[pattern] = count
				print("Received: ", pattern, " Count: ", count)
			## increment the index variable for the patterns
			x += n

		return name_counts

if __name__ == '__main__':
	## check the patterns in the text
	name_counts = check_patterns("task1_3_text.txt", "task1_3_names.txt", verbose=True, force=None)

	## convert the dictionary to a list of tuples
	l_counts = list(name_counts.items())
	## convert the list of tuples to a string
	str_counts =str(l_counts)

	#remove brackets
	str_counts = str_counts.replace("[", "")
	str_counts = str_counts.replace("]", "")

	## print the counts as tuples like requested
	print(str_counts)

	## write the tuples to a file
	with open("task1_3_output.txt", "w", encoding='utf8') as f:
		f.write(str_counts)


#naieve output
##('Harry', 3991), ('Ron', 1185), ('Hermione', 1217), ('Hagrid', 168), ('Dumbledore', 588), ('Draco', 62), ('McGonagall', 70), ('Snape', 292), ('Gilderoy', 0), ('Ginny', 122), ('Malfoy', 89), ('Vernon', 50), ('Arthur', 20), ('Molly', 11), ('Sirius', 69), ('Remus', 21), ('Peter', 2), ('Neville', 89), ('Fred', 94), ('George', 77), ('Moody', 30), ('Cho', 13), ('Voldemort', 446), ('Bellatrix', 98), ('Luna', 140)
#kpm
##('Harry', 3991), ('Ron', 1185), ('Hermione', 1217), ('Hagrid', 168), ('Dumbledore', 588), ('Draco', 62), ('McGonagall', 70), ('Snape', 292), ('Gilderoy', 0), ('Ginny', 122), ('Malfoy', 89), ('Vernon', 50), ('Arthur', 20), ('Molly', 11), ('Sirius', 69), ('Remus', 21), ('Peter', 2), ('Neville', 89), ('Fred', 94), ('George', 77), ('Moody', 30), ('Cho', 13), ('Voldemort', 446), ('Bellatrix', 98), ('Luna', 140)

##expected output
##('Harry', 3991), ('Ron', 1185), ('Hermione', 1217), ('Hagrid', 168), ('Dumbledore', 588), ('Draco', 62), ('McGonagall', 70), ('Snape', 292), ('Gilderoy', 0), ('Ginny', 122), ('Malfoy', 89), ('Vernon', 50), ('Arthur', 20), ('Molly', 11), ('Sirius', 69), ('Remus', 21), ('Peter', 2), ('Neville', 89), ('Fred', 94), ('George', 77), ('Moody', 30), ('Cho', 13), ('Voldemort', 446), ('Bellatrix', 98), ('Luna', 140)
