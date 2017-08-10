import sys

write=sys.stdout.write

def main():
	cnt = 0
	
	for line in sys.stdin:
		write(line)
		cnt += 1
		if cnt >= 10:
			break
		

if __name__ == '__main__':
	main()

