

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






def generate_passwords(length):

	password_list = []


	if length == 4:
		for x in range(2):
			start_type = values[x]
			for y in range(4):
				if y != x:
					second_char = values[y]
				else:
					continue
				for z in range(4):
					if z != x and z != y:
						third_char = values[z]
					else:
						continue
					for a in range(4):
						if a != x and a != y and a != z:
							fourth_char = values[a]
						else:
							continue

						for i in range(len(start_type)):
							for j in range(len(second_char)):
								for k in range(len(third_char)):
									for l in range(len(fourth_char)):
										password = start_type[i] + second_char[j] + third_char[k] + fourth_char[l]
										password_list.append(password)
	return password_list


			

			


					







passwords = generate_passwords(length)

print(passwords)
print(len(passwords))

