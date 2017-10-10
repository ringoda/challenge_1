from __future__ import print_function
import time

start_time = time.time()

with open('a_article.txt') as f_input:
	with open('clean_a_articles.txt', 'w') as f_output:
		for line in f_input:
			if line[0:len('#redirect')] != '#redirect':
				print(line, file=f_output, end="")

end = time.time()

print('Run time: ' + str(end-start_time))