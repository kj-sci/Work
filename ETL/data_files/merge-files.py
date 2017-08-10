# -*- coding: utf-8 -*-
import sys
import re
import glob
write = sys.stdout.write

class merge_files:
	def __init__(self):
		self.loop = 1

	def process(self, fname, flg):
		fp = open(fname, 'r')
		header_str = fp.readline()
		header = unicode(header_str, 'cp932').split('\t')
		num_fields = len(header)
		if flg == 0:
			write('ROW_ID\tFILE_ID\t')
			write(header_str)
			self.field_name = header
			self.num_fields = num_fields
		else:
			if self.num_fields <> num_fields:
				sys.stderr.write('Error: num_fields = '+str(num_fields)+' (expected '+str(self.num_fields)+')\n')
				sys.exit(1)
			for loop1 in range(num_fields):
				if self.field_name[loop1] != header[loop1]:
					sys.stderr.write('Error: field_name['+str(loop1)+'] = '+header[loop1].encode('cp932')+' (expected'+self.field_name[loop1].encode('cp932')+')\n')
					sys.exit(1)
		
		for line in fp:
			line_u = unicode(line, 'cp932')
			data = line_u[:-1].split('\t')
			write(str(self.loop))
			write('\t')
			write(str(flg+1))
			for loop in range(num_fields):
				write('\t')
				data[loop] = re.sub('\$null\$', '', data[loop])
				write(data[loop].encode('cp932'))
			#write(line)
			write('\n')
			
			self.loop += 1

		fp.close()

	def get_recs(self):
		return self.loop

		
def main():
	if len(sys.argv) < 3:
		sys.stderr.write('Usage: python merge-files.py (dirname) (suffix(txt/tab/tsv/etc.)) [num_fields]\n')
		sys.exit(1)

	dirname = sys.argv[1]
	file_suffix = sys.argv[2]
	#num_fields = int(sys.argv[2])
	
	file_match_str = dirname + '\\*.' + file_suffix
	#sys.stderr.write('Glob '+file_match_str+'\n')
	
	hd = merge_files()
	
	file_list = glob.glob(file_match_str)
	loop = 0
	for filename in file_list:
		sys.stderr.write(str(loop+1)+"\t"+filename+"\n")
		hd.process(filename, loop)
		loop += 1

	#sys.stderr.write("#Records: "+str(hd.get_recs())+'\n')
	
if __name__ == '__main__':
	main()
