from __future__ import print_function
import time


#start time measure
start_time = time.time()

#our function that finds matches in a given article using only indexing
cdef everything(index_list, word_list, num_list):
	#define all variables we need to use
	cdef int index = 0
	cdef list indices = [0] * len(index_list)
	cdef int num_of_lists = len(index_list) - 1
	cdef list num_of_words = [len(y) - 1 for y in index_list]
	done = False
	cdef list results = []
	while not done:
		try:
			if (num_list[index][0]) <= (index_list[index+1][indices[index+1]] - len(word_list[index]) - index_list[index][indices[index]]) <= (num_list[index][1]):
				if index + 1 == num_of_lists:
					results.append(((index_list[0][indices[0]]), (index_list[index+1][indices[index+1]]+len(word_list[index+1])) ))
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
				else:
					index += 1
			else:
				if indices[index+1] == num_of_words[index+1]:
					if indices[index] == num_of_words[index]:
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
							indices[index+1] = 0
							indices[index] += 1
							if index == 0:
								continue
							else:
								index -= 1
				else:
					indices[index+1] += 1

		except IndexError:
			#for debugging purposes
			import pdb; pdb.set_trace()
	return set(results)


#this string to your search pattern
cdef str string_input = '"stress" [0,250] "test"'

#parse the search pattern
cdef list list_of_words = string_input.split('"')
cdef list final = [x for x in list_of_words if len(x) and '[' not in x]
cdef int counter = 0
cdef list final_nums = [x for x in list_of_words if len(x) and '[' in x]
final_nums = [x.replace(' ', '') for x in final_nums]
final_nums = [x.replace('[', '') for x in final_nums]
final_nums = [x.replace(']', '') for x in final_nums]
final_nums = [x.split(',') for x in final_nums]
for list_of_num in range(len(final_nums)):
	for nums in range(len(final_nums[list_of_num])):
		final_nums[list_of_num][nums] = int(final_nums[list_of_num][nums])

#here we will gather the results
cdef list query_res = []

#specify file to search in
with open('clean_wiki_data.txt') as f_input:
	for line_1 in f_input:
		if True:
			if all(x in line_1 for x in final):
				list_of_lists = []
				line = line_1.decode('utf-8')
				for i in final:
					start = 0
					result = []
					while True:
						start = line.find(i, start)
						if start == -1: break
						result.append(start)
						start += len(i)
					list_of_lists.append(result)

				len_before = len(query_res)

				sub_result = everything(list_of_lists, final, final_nums)
				if sub_result:
					[query_res.append(line[x[0]:x[1]].encode('utf-8')) for x in sub_result]
				
				if(len_before < len(query_res)):
					counter += 1

print(len(query_res))
print(counter)
#for i in query_res:
#	print(i)
end = time.time()

#print('Run time: ' + str(end-start_time))