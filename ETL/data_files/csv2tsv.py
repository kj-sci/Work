import sys
import csv
import re

write = sys.stdout.write
outdelim = '\t'
eol = '\n'

#code_in = 'cp932'
#code_out = 'cp932'

class csv_handler:
	def __init__(self):
		self.seqno = 1
		
	def process(self):
		csv_hd = csv.reader(sys.stdin, delimiter=',', quotechar='"')
		# loop: index in the file
		loop = 0
		for row in csv_hd:
			if loop == 0:
				loop += 1
				
				# header
				if self.seqno == 1:
					self.num_fields = len(row)
					write('seqno')
					for item in row:
						write(outdelim)
						write(item)
					write(eol)
				continue
			elif(loop % 100000 == 0):
				sys.stderr.write(str(loop)+eol)

			idx = 0

			# output to file
			write(str(self.seqno))
			self.seqno += 1
			for item in row:
				write(outdelim)
				m = re.search('\t', item)
				if m is not None:
					sys.stderr.write(str(self.seqno)+'['+str(idx)+']: ('+item+')\n')
					item = item.replace(outdelim, '<TAB>')
				write(item)
				idx += 1
			write(eol)

			# data check
			if idx != self.num_fields:
				sys.stderr.write('Error: (row, num_fields)=('+str(loop)+', '+str(idx)+')\n')
				
				self.sample_print(row)
				sys.exit(1)

			loop += 1
		

	def sample_print(self, row):
		print '----------------------------------------------------'
		loop = 0
		for item in row:
			print loop, ": ", item
			loop += 1

def main():
	hd = csv_handler()
	hd.process()
	
if __name__ == '__main__':
	main()
	
