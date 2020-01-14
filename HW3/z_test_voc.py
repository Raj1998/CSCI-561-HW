import sys
import os

def readoutput(filename):
	answer=[]
	file = open(filename,'r')
	data = file.readlines()
	for line in data:
		answer.append(line.rstrip())
	
	# if answer[-1]=='':
	# 	return answer[:-1]

	return answer

def ansCheck(truth,stdoutput):
	truth=readoutput(truth)
	stdans=readoutput(stdoutput)
	if truth == stdans:
		return True
	else:
		return False
	# if len(truth)!=len(stdans):
	# 	return ['D',truth,stdans]
	# diff=[i+1 for i in range(len(truth)) if (truth[i]=='FAIL' and stdans[i]!='FAIL')or(truth[i]!='FAIL' and stdans[i]=='FAIL') ]
	# return diff

if __name__ == "__main__":
	#compare two output
	#print PASS or give wrong line number
	
	p = 0
	f = 0
	for i in range(1, 50 + 1):
		input_file = f'testcases/input_{i}.txt'
		os.system(f'python3 auto_submit.py {input_file}')
		result=ansCheck(f'./testcases/output_{i}.txt','output.txt')
		if result:
			print(f'Testcase {i} --- PASS')
			p+=1
		else:
			print(f'Testcase {i} -Failllllllllll')
			f+=1
	print(p, f)
		# elif result[0]=='D':
		# 	print('More or Less lines in the your answer')
		# 	print(result[1])
		# 	print(result[2])
		# else:
		# 	print('Wrong line number:')
		# 	for i in range(len(result)):
		# 		print(result[i])