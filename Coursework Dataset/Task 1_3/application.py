import multiprocessing as mp



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
	# print(count)
	result_queue.put((pattern, count))


def read_files():
	with open("task1_3_text.txt", "r", encoding='utf8') as f:
		text = f.read()

	with open("task1_3_names.txt", "r", encoding='utf8') as f:
		patterns = f.readlines()

	# remove newline characters
	patterns = [x.strip() for x in patterns]

	return text, patterns


def check_capacity():
	# print number of processors
	if mp.cpu_count() < 4:
		# print("Number of processors is less than 4")
		n = 1
	elif mp.cpu_count() < 8:
		# print("Number of processors is less than 8")
		n = 2
	else:
		# print("Number of processors is greater than 8")
		n = 4

	return n


def check_patterns(patterns, text, n):
	result_queue = mp.Queue()
	x = 0

	name_counts = {}

	while x < len(patterns):
		# print("round start")
		process_list = []
		if n > (len(patterns) - x):
			stop = x + (len(patterns) - x)
		else:
			stop = x + n

		for i in range(x, stop):
			# print("pattern: " + patterns[i])
			p = mp.Process(target=search, args=(patterns[i], text, result_queue))
			process_list.append(p)

		for p in process_list:
			p.start()

		for p in process_list:
			p.join()

		while not result_queue.empty():
			pattern, count = result_queue.get()
			name_counts[pattern] = count

		x += n
	return name_counts

if __name__ == '__main__':
	text, patterns = read_files()
	n = check_capacity()
	name_counts = check_patterns(patterns, text, n)
	l_counts = list(name_counts.items())
	str_counts =str(l_counts)

	#remove brackets
	str_counts = str_counts.replace("[", "")
	str_counts = str_counts.replace("]", "")
	

	with open("task1_3_output.txt", "w") as f:
		f.write(str_counts)

	print(str_counts)
