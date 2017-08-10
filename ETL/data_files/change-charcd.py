# -*- coding: utf-8 -*-

import sys
import re

write = sys.stdout.write

class change_char_cd:
	def __init__(self, incode, outcode, indelim, outdelim):
		if indelim == 'tab':
			self.indelim = '\t'
		else:
			self.indelim = indelim
		
		if outdelim == 'tab':
			self.outdelim = '\t'
		else:
			self.outdelim = outdelim

		self.eol = '\n'
		
		self.incode = incode
		self.outcode = outcode
		
		self.num_fields = 0
		

	def process(self):
		# process data
		cnt = 0
		for line in sys.stdin:
			line_u = unicode(line, self.incode)
			data = line_u[:-1].split(self.indelim)
			
			if cnt == 0:
				self.num_fields = len(data)

			# Temporaray
			m = re.search('^([^\.]*)\.0*$', data[0])
			if m is not None:
				data[0] = m.group(1)
				
			for loop in range(len(data)):
				if loop > 0:
					write(self.outdelim)
				write(data[loop].encode(self.outcode))
			write(self.eol)
				
			cnt += 1

			if cnt % 1000 == 0:
				sys.stderr.write(str(cnt)+'\n')

		
			

def main():
	if len(sys.argv) < 5:
		sys.stderr.write('Usage: cat datafile | python $0 incode(e.g. utf8) outcode(e.g. cp932) indelim(tab/,/etc.) outdelim(tab/,/etc.) > outfile\n')
		sys.exit(1)
	
	incode = sys.argv[1]
	outcode = sys.argv[2]
	indelim = sys.argv[3]
	outdelim = sys.argv[4]
	
	hd = change_char_cd(incode, outcode, indelim, outdelim)
	hd.process()


	
if __name__ == '__main__':
	main()


		