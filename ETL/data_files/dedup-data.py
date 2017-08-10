import sys

write=sys.stdout.write


def process(indelim, outdelim, key_idx_list):
	cnt = 0
	prev_key = ''
	for line in sys.stdin:
		#line_u = line #unicode(line, 'cp932')
		line_u = unicode(line, 'cp932')
		data = line_u[:-1].split(indelim)
		if cnt % 10000 == 0:
			sys.stderr.write(str(cnt)+"\n")
		cnt += 1
		
		this_key = ''
		for loop in range(len(key_idx_list)):
			this_key += data[key_idx_list[loop]]

		if this_key == prev_key:
			sys.stderr.write('Duplicate: '+line)
			continue
		
		write(line)
		prev_key = this_key
		

def main():
	if len(sys.argv) < 2:
		sys.stderr.write("Usage: cat datafile | python dedup-data.py (key_idx_list(csv)) [indelim] > outfile\n")
		sys.exit(1)

	key_idx_list_chr = sys.argv[1].split(',')
	key_idx_list = []
	for item in key_idx_list_chr:
		key_idx_list.append(int(item))
	
	sys.stderr.write("Key fields: "+'|'.join(key_idx_list_chr)+'\n')
	
	if len(sys.argv) >= 3:
		indelim = sys.argv[2]
	else:
		indelim = '\t'
		
	outdelim = '\t'

	process(indelim, outdelim, key_idx_list)

if __name__ == '__main__':
	main()
	
		