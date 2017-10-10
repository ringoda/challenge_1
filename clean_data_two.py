from __future__ import print_function
import time

start = time.time()


bReading = False
correct_ns = False

ns_sign = '<ns>0</ns>'
begin_sign = '<text xml:space="preserve">'
end_sign = '</text>'

with open('enwiki-20170820-pages-articles-multistream.xml') as f_input:
	with open('final_wiki_red.txt', 'w') as f_output:
			for line in f_input:
				if not correct_ns:
					if ns_sign in line:
						correct_ns = True
				else:
					if not bReading:
						if begin_sign in line:
							bReading = True
							new_line = line[line.index(begin_sign)+len(begin_sign):]
							if end_sign in line:
								bReading = False
								correct_ns = False
								result = new_line[:new_line.index(end_sign)].replace('\n', ' ')
								print(result.lower(), file=f_output)
					else:
						new_line += line
						if end_sign in line:
							bReading = False
							correct_ns = False
							result  = new_line[:new_line.index(end_sign)].replace('\n', ' ')
							print(result.lower(), file=f_output)
end = time.time()

#print the runtimes which is found by subtracting end time from start time
print ('Python runtime: ' + str(end - start))


