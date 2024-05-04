

capitals = ['A', 'B', 'C', 'D', 'E']
small = ['a', 'b', 'c', 'd', 'e']
numbers = ['1', '2', '3', '4', '5']
special = ['$', '&', '%']


values = [capitals, small, numbers, special]


# it must include at least one element from each category;
# it must start with letters (capital or lower-case);
# it must not include more than two capital letters;
# it must not include more than two special symbols.


length = int(input("Enter the password length: "))
print_values = True if input("Do you want to print the values? (1/0): ") == "1" else False


if length < 4:
	print("Password length must be at least 4 or all categories will not be included.")
	exit()



## testing
# def generate_passwords(length):

# 	password_list = []


# 	
	# for x in range(2):
	# 	start_type = values[x]
	# 	for y in range(4):
	# 		if y != x:
	# 			second_char = values[y]
	# 		else:
	# 			continue
	# 		for z in range(4):
	# 			if z != x and z != y:
	# 				third_char = values[z]
	# 			else:
	# 				continue
	# 			for a in range(4):
	# 				if a != x and a != y and a != z:
	# 					fourth_char = values[a]
	# 				else:
	# 					continue

	# 				for i in range(len(start_type)):
	# 					for j in range(len(second_char)):
	# 						for k in range(len(third_char)):
	# 							for l in range(len(fourth_char)):
	# 								password = start_type[i] + second_char[j] + third_char[k] + fourth_char[l]
	# 								password_list.append(password)

# 	return password_list

password_list = []


def rec_gen(prefix, remaining_length, counts):
	if remaining_length == 0:
		# Check if the password meets the requirements
		if prefix[0] not in values[0] and prefix[0] not in values[1]:
			return
		if 0 in counts:
			return
		if counts[0] > 2 or counts[3] > 2:
			return
		
		password_list.append("".join(prefix))
		return

	for i in range(4):
		new_counts = counts.copy()
		new_counts[i] += 1
		for char in values[i]:
			new_prefix = prefix + [char]
			rec_gen(new_prefix, remaining_length - 1, new_counts)


rec_gen([], length, [0, 0, 0, 0])

if print_values:
	for i, password in enumerate(password_list):
		print(f"{i+1} {password}")

print(len(password_list))
					

