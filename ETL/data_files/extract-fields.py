import sys

write=sys.stdout.write


def process(indelim, outdelim, extract_idx_list):
	cnt = 0
	for line in sys.stdin:
		#line_u = line #unicode(line, 'cp932')
		line_u = unicode(line, 'cp932')
		data = line_u[:-1].split(indelim)
		if cnt % 10000 == 0:
			sys.stderr.write(str(cnt)+"\n")
		cnt += 1
		

		for loop in range(len(extract_idx_list)):
			if loop > 0:
				write(outdelim)
					
			write(data[extract_idx_list[loop]].encode('cp932'))
		write('\n')

		'''
		if cnt == 1:
			print 'site_id\tpage_id\turl\tphone_no_1\tphone_no_2'
		else:
			for loop in range(len(extract_idx_list)):
				if loop > 0:
					write(outdelim)
					
				if loop == 4:
					data[extract_idx_list[loop]] = data[extract_idx_list[loop]][1:]
				
				write(data[extract_idx_list[loop]])
				#write(data[extract_idx_list[loop]].encode('cp932'))
			write('\n')
		'''

def main():
	if len(sys.argv) < 2:
		sys.stderr.write("Usage: cat datafile | python extract-fields.py (extract_idx_list(csv)) [indelim] > outfile\n")
		sys.exit(1)

	extract_idx_list_chr = sys.argv[1].split(',')
	extract_idx_list = []
	for item in extract_idx_list_chr:
		extract_idx_list.append(int(item))
	
	sys.stderr.write("Extract fields: "+'|'.join(extract_idx_list_chr)+'\n')
	
	if len(sys.argv) >= 3:
		indelim = sys.argv[2]
	else:
		indelim = '\t'
		
	outdelim = '\t'

	process(indelim, outdelim, extract_idx_list)

if __name__ == '__main__':
	main()
	
		