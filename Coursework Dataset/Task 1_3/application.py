import multiprocessing as mp
import os


def search(pattern, text):
	count = 0

	for i in range(len(text)-len(pattern)+1):
		
		if text[i] == pattern[0]:
			found = True
			for j in range(1, len(pattern)):
				if text[i+j] != pattern[j]:
					found = False
					break
			if found:
				count += 1

	return count


with open("task1_3_text.txt", "r", encoding='utf8') as f:
	text = f.read()
    




hNumber = search("Ron", text)

print("Number of times Harry appears in the text: ", hNumber)