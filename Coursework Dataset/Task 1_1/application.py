
## Define the Char sets for the password
capitals = ['A', 'B', 'C', 'D', 'E']
small = ['a', 'b', 'c', 'd', 'e']
numbers = ['1', '2', '3', '4', '5']
special = ['$', '&', '%']

## Define the Char categories
values = [capitals, small, numbers, special]

## Get the length a password should be
length = int(input("Enter the password length: "))
## Ask if the user wants to print all passwords
print_values = True if input("Do you want to print the created passwords? (1/0): ") == "1" else False


## check if the length meets the infered requrement (4 Char categories which must all be used at least once)
if length < 4:
	print("Password length must be at least 4 or all categories will not be included.")
	exit()

# Define list to store recursive generations
password_list = []

## Recursive function to generate all possible passwords
## The prefix should start as an empty list
## The remaining length should start as the length of the password
## The counts should start as an array of Zeros, matching the number of categories
def rec_gen(prefix, remaining_length, counts):

	## 5.	If remaining length not 0 GOTO step 6
	if remaining_length == 0:
		# Check if the password meets the requirements
		## 5.1.	If first character in PREFIX is not from CAPITAL or SMALL set
		if prefix[0] not in values[0] and prefix[0] not in values[1]:
			## GOTO 6.5.4.
			return
		## 5.2.	If any COUNTS is 0
		if 0 in counts:
			## GOTO 6.5.4.
			return
		## 5.3.	If there are more than two CAPITALS or SPECIALS
		if counts[0] > 2 or counts[3] > 2:
			## GOTO 6.5.4.
			return
		## 5.4.	Append PASSWORD LIST with PREFIX
		password_list.append("".join(prefix))
		## 5.5.	GOTO 6.5.4.
		return

	## 6.	If INDEX is greater than number of TYPES, GOTO 7
	for i in range(len(values)):
		## 6.1.	Create a copy of COUNTS array as NEW COUNTS.
		new_counts = counts.copy()
		## 6.2.	Offset NEW COUNTS by INDEX and increment the value by one.
		new_counts[i] += 1
		## 6.3.	Set TYPE to the offset of TYPES by INDEX.
		## 6.4.	Increment INDEX by one
		## 6.5.	If INDEX2 is greater than the number of characters in TYPE, GOTO 6
		for char in values[i]:
			## 6.5.1.	Append PREFIX with a character by offsetting the TYPE by INDEX2.
			new_prefix = prefix + [char]
			## 6.5.2.	Increment INDEX2 by one.
			## 6.5.3.	Negate one from REMAINING LENGTH.
			## 6.5.4.	GOTO 5.
			rec_gen(new_prefix, remaining_length - 1, new_counts)


rec_gen([], length, [0, 0, 0, 0])

if print_values:
	for i, password in enumerate(password_list):
		print(f"{i+1} {password}")

print(f"L = {length}, N = {len(password_list)}")
