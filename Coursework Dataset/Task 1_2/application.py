
#																								<a, b, a, b, c, c, b>
#																							['f', 'k', 'c', 'f', 'f', 'j', 'a', 'i', 'e', 'j', 'f', 'f', 'f', 'b', 'g', 'h', 'f', 'j', 'j', 'd']
#																					   ['d', 'f', 'k', 'c', 'f', 'f', 'j', 'a', 'i', 'e', 'j', 'f', 'f', 'f', 'b', 'g', 'h', 'f', 'j', 'j']


#																						['j', 'j', 'g', 'i', 'b', 'j', 'i', 'b', 'j', 'e', 'j', 'a', 'i', 'i', 'j', 'c', 'b', 'i', 'j', 'b', 'b', 'f']
#																				['d', 'd', 'd', 'i', 'a', 'b', 'c', 'a', 'j', 'd', 'g', 'd', 'k', 'd', 'i', 'h', 'i', 'd', 'e', 'f', 'i', 'i']
#																				['d', 'f', 'k', 'c', 'f', 'f', 'j', 'a', 'i', 'e', 'j', 'f', 'f', 'f', 'b', 'g', 'h', 'f', 'j', 'j', 'd', 'd']

#																				['i', 'g', 'd', 'g', 'j', 'b', 'k', 'd', 'g', 'i', 'i', 'g', 'j', 'a', 'j', 'i', 'i', 'g', 'd', 'f', 'd', 'h', 'i', 'g', 'g', 'c', 'g', 'g', 'd']


def get_text(path):
	##read file in as text
	with open(path, 'r') as file:
		data = file.read()


	return data


def print_freqs(frequencies):
	freq_list = []

	for i in frequencies:
		if frequencies[i] == 1:
			pass
		else:
			freq_list.append((i, frequencies[i]))

	return freq_list

def explode_string(data, locations, length):
	substrings = []
	for location in locations:
		c_string = []
		for i in range(location, location + length):
			c_string.append(data[i])
		substrings.append(c_string)

		
	return substrings


#print all subsrings found
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





def longest_substring(startpos, text, k):
	## rule for substring: only k elements are allowed to repeat, but they can repeat as many times as possible
 
	
	##initialize variables
	height = 0
	height_pos = []
	frequencies = []

	
	##iterate through the text
	for i in range(startpos, len(text)):
		chars = {}

		for j in range(i, len(text)):
			##if the character is not in the dictionary, add it
			if text[j] not in chars:
				chars[text[j]] = 1
			else:
				chars[text[j]] += 1

			
			## check number of chars that repeat
			k_count = 0
			for key in chars:
				if chars[key] != 1:
					k_count += 1

			length = j - i + 1
			
			if k_count == k:

				if length > height:
					height = length
					height_pos = [i]
					frequencies.clear()
					frequencies.append(chars.copy())

				elif length == height:
					height_pos.append(i)
					frequencies.append(chars.copy())
				

			elif k_count < k:
				pass
			else:
				break

	return height, height_pos, frequencies
			



k = int(input("Enter the value of k: "))

data = get_text('letters.txt')


lengths, positions, frequencies = longest_substring(0, data, k)


printout(lengths, positions, frequencies, data)



