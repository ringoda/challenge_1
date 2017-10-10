from __future__ import print_function
import time

#start time measure
start_time = time.time()

#our function that finds matches in a given article using only indexing
def everything(index_list, word_list, num_list):
	#define all variables we need to use
	index = 0
	indices = [0] * len(index_list)
	num_of_lists = len(index_list) - 1
	num_of_words = [len(y) - 1 for y in index_list]
	done = False
	results = []
	
	#we want to keep looping until we have checked all possible matches
	while not done:
		#simple, try...except here for debugging purposes
		try:
			#the way we do this is by checking the distance between words number index and index + 1 and see if that matches
			#the given interval from numlist

			#here we compare the two neighbouring values and we either:
			if (num_list[index][0]) <= (index_list[index+1][indices[index+1]] - len(word_list[index]) - index_list[index][indices[index]]) <= (num_list[index][1]):
				#The latter word is the last word in the list: We gather the result and start again
				if index + 1 == num_of_lists:
					results.append(((index_list[0][indices[0]]), (index_list[index+1][indices[index+1]]+len(word_list[index+1])) ))
					#we need to make sure to leave all lists and indexes in the correct state before beginning again
					#we therefore loop through all indices and check them if they need to be changed or incremented
					#and likewise to which point we should move the index
					for j in range(num_of_lists,-1,-1):
						if indices[j] < num_of_words[j]:
							indices[j] += 1
							if j == 0:
								index = 0
							else:
								index = j-1
							break
						else:
							if j == 0:
								#flip the flag
								done = True
								#we are finished
								break
							indices[j] = 0
				#The latter word is not the last word: We then check the next two values (increment index)
				else:
					index += 1
					 
			else:
				#The index for the latter word is the last index for that word in the article
				if indices[index+1] == num_of_words[index+1]:
					#The index for the first word is the last index for that word in the article
					if indices[index] == num_of_words[index]:
						#we need to make sure to leave all lists and indexes in the correct state before beginning again
						#we therefore loop through all indices and check them if they need to be changed or incremented
						#and likewise to which point we should move the index
						for j in range(index+1,-1,-1):
							if indices[j] < num_of_words[j]:
								indices[j] += 1
								if j == 0:
									index = 0
								else:
									index = j-1
								break
							else:
								if j == 0:
									#flip the flag
									done = True
									#we are finished
									break
								indices[j] = 0
					else:
							#we increment the first word and reset the latter word and move the index one step back
							indices[index+1] = 0
							indices[index] += 1
							#if we are at the first word we don't need to move the index
							if index == 0:
								continue
							else:
								index -= 1
				else:
					#we increment the index of the latter word
					indices[index+1] += 1

		#catch out of index errors for debugging
		except IndexError:
			#for debugging purposes
			import pdb; pdb.set_trace()
	#return the results we no exact duplicates
	return set(results)


#this string to your search pattern
string_input = '"first" [0,85] "letter" [0,100] "alphabet" [0, 200] "consonant"'

#parse the search pattern
list_of_words = string_input.split('"')
final = [x for x in list_of_words if len(x) and '[' not in x]
counter = 0
final_nums = [x for x in list_of_words if len(x) and '[' in x]
final_nums = [x.replace(' ', '') for x in final_nums]
final_nums = [x.replace('[', '') for x in final_nums]
final_nums = [x.replace(']', '') for x in final_nums]
final_nums = [x.split(',') for x in final_nums]
for list_of_num in range(len(final_nums)):
	for nums in range(len(final_nums[list_of_num])):
		final_nums[list_of_num][nums] = int(final_nums[list_of_num][nums])

#here we will gather the results
query_res = []

#specify file to search in
with open('clean_a_articles.txt') as f_input:
	#loop through the lines(articles)
	for line_1 in f_input:
		#we first check if the line has all the words we search for
		#if not we just go straight to the next line(article)
		if all(x in line_1 for x in final):
			list_of_lists = []
			#we need the right character encoding
			line = line_1.decode('utf-8')
			#here we loop through the words and gather the indexes
			#of all occurences of all words
			for i in final:
				start = 0
				result = []
				while True:
					start = line.find(i, start)
					if start == -1: break
					result.append(start)
					start += len(i)
				list_of_lists.append(result)

			#this is simply used to count the articles we found matches in
			len_before = len(query_res)

			#here we call the function that does all the heavy lifting
			sub_result = everything(list_of_lists, final, final_nums)
			#if we got any matches we append them to the query_res
			if sub_result:
				[query_res.append(line[x[0]:x[1]].encode('utf-8')) for x in sub_result]
			
			#again using the length of the end result to count number of results
			if(len_before < len(query_res)):
				counter += 1
#print matches and resulst
print(len(query_res))
print(counter)
#uncomment next two lines to see actual matches
#for i in query_res:
	#print(i)

#stop measuring time
end = time.time()

#print runtime
print('Run time: ' + str(end-start_time))