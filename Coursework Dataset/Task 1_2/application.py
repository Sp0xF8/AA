
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


def printout(lengths, positions, data):
	print("The longest substring of length", k, "is/are:")
	for i in range(len(lengths)):
		print(data[positions[i]:positions[i] + lengths[i]])
		print("Position:", positions[i], "Length:", lengths[i])




def longest_substring(text, k):
	## create a dictionary to store the frequency of each character
	character_frequency = {}
	## create a list to be used as a queue
	queue = []
	
	sub_string_lengths = []
	sub_string_positions = []

	## loop through each character in the text
 
	for i in range(len(text)):
		### check if the character is not in the dictionary
		if text[i] not in character_frequency:
			#### create an empty list for the character
			character_frequency[text[i]] = []
		


	return sub_string_lengths, sub_string_positions



k = int(input("Enter the value of k: "))

data = get_text('letters.txt')


lengths, positions = longest_substring(data, k)

printout(lengths, positions, data)



