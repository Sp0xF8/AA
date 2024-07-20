
def get_text(path):
	##read file in as text
	with open(path, 'r') as file:
		data = file.read()


	return data

## convert the dictionary of frequencies to a list of tuples of characters and their frequencies
def print_freqs(frequencies):
	## initialize the list to store the tuples
	freq_list = []
	## for each key in the dictionary
	for i in frequencies:
		## if the value is 1, pass
		if frequencies[i] == 1:
			pass
		## else the value must be greater than 1, append the key and value as a tuple to the list
		else:
			freq_list.append((i, frequencies[i]))

	## return the list of tuples
	return freq_list

## takes data and a list of positions and a length to return a list of substrings as lists of characters
def explode_string(data, locations, length):
	substrings = []
	## for each location in the list of positions
	for location in locations:
		## create a list to store the substring
		c_string = []
		## for each character in the string
		for i in range(location, location + length):
			## append the character to the list
			c_string.append(data[i])
		## append the built string to the list of substrings
		substrings.append(c_string)

		
	return substrings

#print all subsrings found in format requested
def printout(lengths, positions, frequencies, data):

	initString = str("k=" + str(k) + ", longest substring is " + str(lengths) + ",")

	print(initString, end="")

	substrings = explode_string(data, positions, lengths)

	data_len = len(data)



	for i in range(len(positions)):
		if i == 0:
			print(f" {substrings[i]} with the frequency {print_freqs(frequencies[i])} at position {positions[i]}/{data_len}")
		else:
			print(len(initString) * " ", f"{substrings[i]} with the frequency {print_freqs(frequencies[i])} at position {positions[i]}/{data_len}")


		# print("Substring:", substrings[i])
		# print("Position:", positions[i], "Length:", lengths)
		# print("Frequencies:", list(print_freqs(frequencies[i])))

def longest_substring(text, k):	
	##initialize variables
	height = 0
	## store the position of the longest substring instead of the substring itself. Combine with the height to get the substring
	height_pos = []
	## store the frequencies of the characters in the substring relative to the string at the same offset as the height_pos
	frequencies = []

	
	##iterate through the text
	for i in range(len(text)):
		## store the characters in the substring
		chars = {}
		## iterate through the text from the current position of WINDOW POS, using j as CURRENT POS
		for j in range(i, len(text)):
			## check if the character at CURRENT POS is in the dictionary keys
			if text[j] not in chars:
				## if not, add it to the dictionary and set the value to 1
				chars[text[j]] = 1
			else:
				## if it is, increment the value by one
				chars[text[j]] += 1

			
			## check number of chars that repeat
			k_count = 0
			## for each key in the dictionary
			for key in chars:
				## if the value is not 1, increment the count
				if chars[key] != 1:
					k_count += 1

			## calculate the length of the substring by subbing the CURRENT POS from the WINDOW POS and adding 1
			length = j - i + 1
			
			## check if the number of repeating characters is equal to k
			if k_count == k:

				## check if the length of the substring is greater than the current height
				if length > height:
					## if it is, set the height to the length of the substring
					height = length
					## set the height position to a list with the current position
					height_pos = [i]
					## clear the frequencies list and add the current dictionary of characters
					frequencies.clear()
					frequencies.append(chars.copy())
				## if the length is equal to the height
				elif length == height:
					## append the string positions with the current position
					height_pos.append(i)
					frequencies.append(chars.copy())
				
			## else, if the number of repeating characters is less than k
			elif k_count < k:
				## contineu to the next CURRENT POS
				pass
			## if the number of repeating characters is greater than k,
			else:
				## break the loop and move to the next WINDOW POS
				break
	return height, height_pos, frequencies


k = int(input("Enter the value of k: "))

data = get_text('letters.txt')


lengths, positions, frequencies = longest_substring(data, k)


printout(lengths, positions, frequencies, data)



