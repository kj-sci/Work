import sys
import csv
import re

write=sys.stdout.write

def clean_str(str):
	str = re.sub('\n', '', str)
	
	return str

def process(fname, indelim, outdelim, incode, outcode, extract_idx_list):
	cnt = 0

	f = open(fname, 'r')
	reader = csv.reader(f, delimiter=indelim)
	
	loop1 = 1
	for row in reader:
		if loop1 == 1:
			num_fields = len(row)
		else:
			if num_fields <> len(row):
				sys.stderr.write("Error in row: "+str(loop1)+"\n")
		loop1 += 1
		
		#line_u = line #unicode(line, 'cp932')
		#line_u = unicode(line, 'cp932')
		#data = line_u[:-1].split(indelim)
		if cnt % 10000 == 0:
			sys.stderr.write(str(cnt)+"\n")
		cnt += 1
		

		for loop in range(len(extract_idx_list)):
			if loop > 0:
				write(outdelim)
			value = clean_str(unicode(row[extract_idx_list[loop]], incode))
			write(value.encode(outcode, 'ignore'))
			#write(data[extract_idx_list[loop]].encode('cp932'))
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
	f.close()
		
def main():
	if len(sys.argv) < 7:
		sys.stderr.write("Usage: python extract-fields.py datafile (extract_idx_list(csv)) indelim outdelim incode outcode > outfile\n")
		sys.exit(1)

	fname = sys.argv[1]
	extract_idx_list_chr = sys.argv[2].split(',')
	if sys.argv[3] == 'tab':
		indelim = '\t'
	else:
		indelim = sys.argv[3]
	if sys.argv[4] == 'tab':
		outdelim = '\t'
	else:
		outdelim = sys.argv[4]

	incode = sys.argv[5]
	outcode = sys.argv[6]
	
	extract_idx_list = []
	for item in extract_idx_list_chr:
		extract_idx_list.append(int(item))
	
	sys.stderr.write("Extract fields: "+'|'.join(extract_idx_list_chr)+'\n')
	
	process(fname, indelim, outdelim, incode, outcode, extract_idx_list)

if __name__ == '__main__':
	main()
	
		