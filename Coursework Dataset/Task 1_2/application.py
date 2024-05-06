
#																								<a, b, a, b, c, c, b>
#																							['f', 'k', 'c', 'f', 'f', 'j', 'a', 'i', 'e', 'j', 'f', 'f', 'f', 'b', 'g', 'h', 'f', 'j', 'j', 'd']
#																					   ['d', 'f', 'k', 'c', 'f', 'f', 'j', 'a', 'i', 'e', 'j', 'f', 'f', 'f', 'b', 'g', 'h', 'f', 'j', 'j']


#																						['j', 'j', 'g', 'i', 'b', 'j', 'i', 'b', 'j', 'e', 'j', 'a', 'i', 'i', 'j', 'c', 'b', 'i', 'j', 'b', 'b', 'f']
#																						['d', 'd', 'd', 'i', 'a', 'b', 'c', 'a', 'j', 'd', 'g', 'd', 'k', 'd', 'i', 'h', 'i', 'd', 'e', 'f', 'i', 'i']
#																				['d', 'f', 'k', 'c', 'f', 'f', 'j', 'a', 'i', 'e', 'j', 'f', 'f', 'f', 'b', 'g', 'h', 'f', 'j', 'j', 'd', 'd']

#																				['i', 'g', 'd', 'g', 'j', 'b', 'k', 'd', 'g', 'i', 'i', 'g', 'j', 'a', 'j', 'i', 'i', 'g', 'd', 'f', 'd', 'h', 'i', 'g', 'g', 'c', 'g', 'g', 'd']


def get_text(path):
	##read file in as text
	with open(path, 'r') as file:
		data = file.read()


	return data


#print all subsrings found
def printout(lengths, positions, data):
	print("The longest substring of length", k, "is/are:")
	for i in range(len(lengths)):
		print(data[positions[i]:positions[i] + lengths[i]])
		print("Position:", positions[i], "Length:", lengths[i])




def longest_substring(startpos, text, k):
	## rule for substring: only k elements are allowed to repeat, but they can repeat as many times as possible
 
	
	##initialize variables
	lengths = []
	positions = []

	
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


			##if the most recent length is greater than the previous length, remove all previous lengths
			

			length = j - i + 1
			
			if k_count == k:
				
				if len(lengths) > 1:
					
					prev_length = lengths[-1]
					if length > prev_length:
						lengths.clear()
						positions.clear()
						lengths.append(length)
						positions.append(i)
					elif length == prev_length:
						lengths.append(length)
						positions.append(i)
				else:
					lengths.append(length)
					positions.append(i)
			elif k_count < k:
				continue
			else:
				break

			# if len(lengths) > 1:
			# 	length_index = len(lengths) - 1
			# 	prev_length_index = len(lengths) - 2

			# 	if lengths[length_index] < lengths[prev_length_index]:
			# 		lengths.pop()
			# 		positions.pop()
			# 	elif lengths[length_index] > lengths[prev_length_index]:
			# 		lengths.pop(prev_length_index)
			# 		positions.pop(prev_length_index)

			
			

	return lengths, positions
			



k = int(input("Enter the value of k: "))

data = get_text('letters.txt')


lengths, positions = longest_substring(0, data, k)

##print out the longest substring

printout(lengths, positions, data)



