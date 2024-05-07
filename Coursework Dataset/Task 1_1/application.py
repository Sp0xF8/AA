

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

print(f"L = {length}, N = {len(password_list)}")
