import sys

def main():
	cnt = 0
	
	for line in sys.stdin:
		cnt += 1
		if cnt % 10000 == 0:
			sys.stderr.write(str(cnt)+"\n")
		
	sys.stdout.write("cnt="+str(cnt)+"\n")

if __name__ == '__main__':
	main()

