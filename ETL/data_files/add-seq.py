import sys

write = sys.stdout.write


def simple_process(header_flg, delimiter):
	if header_flg == 'Y':
		header = sys.stdin.readline()
		
		write('ROW_ID')
		write(delimiter)
		write(header)
		
	row_id = 1
	for line in sys.stdin:
		write(str(row_id))
		write(delimiter)
		write(line)
		row_id += 1
		if row_id % 10000 == 0:
			sys.stderr.write(str(row_id)+'\n')
			
	
def complex_process(header_flg, delimiter, jp_fld):
	num_fields = None
	
	if header_flg == 'Y':
		header_str = sys.stdin.readline()
		header = header_str[:-1].split(delimiter)
		num_fields = len(header)
		
		write('ROW_ID')
		write(delimiter)
		write(header_str)
		
	row_id = 1
	for line in sys.stdin:
		data = line[:-1].split(delimiter)
		
		if num_fields is None:
			num_fields = len(data)
			
		write(str(row_id))
		for loop in range(num_fields):
			write(delimiter)
			if jp_fld.has_key(loop):
				data[loop] = unicode(data[loop], 'cp932')
				data[loop] = data[loop].strip()
				data[loop] = data[loop].encode('cp932')
			else:
				data[loop] = data[loop].strip()
				
			write(data[loop])

		write("\n")
		
		if row_id % 10000 == 0:
			sys.stderr.write(str(row_id)+'\n')
		row_id += 1


def pretty_data(str):
	str = str.strip()
	
def main():
	if len(sys.argv) < 2:
		sys.stderr.write("Usage: type datafile | python add-seq.py header_flg(Y/N) (delimiter) > outfile\n")
		sys.exit(1)
	
	header_flg = sys.argv[1]
	if len(sys.argv) >= 3:
		delimiter = sys.argv[2]
	else:
		delimiter = '\t'
	
	simple_process(header_flg, delimiter)

	#jp_fld = {}
	#jp_fld[1] = 1
	#jp_fld[4] = 1
	#jp_fld[6] = 1
	#complex_process(header_flg, delimiter, jp_fld)

if __name__ == '__main__':
	main()
	

	