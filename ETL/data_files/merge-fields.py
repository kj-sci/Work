# -*- coding: utf-8 -*-

import sys
import re
import ky_vars

write = sys.stdout.write

class merge_fields:
	def __init__(self):
		self.ky_vars = ky_vars.ky_vars()
		

	def process(self, flg_header, merged_label, idx_start, idx_end):
		# get header
		if flg_header == '1':
			header_str = unicode(sys.stdin.readline(), self.ky_vars.incode)
			self.field_name = header_str[:-1].split(self.ky_vars.indelim)
			self.num_fields = len(self.field_name)
			loop1 = 0
			for loop in range(self.num_fields):
				if loop >= idx_start and loop < idx_end:
					if loop == idx_start:
						if loop1 > 0:
							write(self.ky_vars.outdelim)
						write(merged_label)
						loop1 += 1
				else:
					if loop1 > 0:
						write(self.ky_vars.outdelim)
					write(self.field_name[loop])
					loop1 += 1
			write('\n')
			
		elif self.flg_header == '0':
			# do nothing.
			pass
		
		#if self.field_name is not None:
		#	print '-----------------------------------'
		#	self.sample_output(self.field_name)
		#	print '-----------------------------------'

		
		# process data
		cnt = 0
		for line in sys.stdin:
			line_u = unicode(line, self.ky_vars.incode)
			data = line_u[:-1].split(self.ky_vars.indelim)
			
			if cnt == 0:
				if flg_header == '0':
					self.num_fields = len(data)
					self.field_name = []
					for loop in range(self.num_fields):
						self.field_name.append('Col_'+str(loop))

			merged_data = ''
			loop1 = 0
			for loop in range(self.num_fields):
				if loop >= idx_start and loop < idx_end:
					merged_data += data[loop]
					if loop == idx_end - 1:
						if loop1 > 0:
							write(self.ky_vars.outdelim)
						write(merged_data.encode(self.ky_vars.outcode))
						loop1 += 1
				else:
					if loop1 > 0:
						write(self.ky_vars.outdelim)
					write(data[loop].encode(self.ky_vars.outcode))
					loop1 += 1

			write('\n')
				
			cnt += 1

			if cnt % 1000 == 0:
				sys.stderr.write(str(cnt)+'\n')
				#break

		
			
	def sample_output(self, data):
		print "------------------------------------------------------------"
		for loop in range(len(data)):
			write('['+str(loop)+'] '+self.field_name[loop].encode(self.ky_vars.outcode)+': '+data[loop].encode(self.ky_vars.outcode))
			write(self.ky_vars.eol)

	
def main():
	if len(sys.argv) < 5:
		sys.stderr.write('Usage: cat datafile | python $0 1(with header)/0(without header) merged_label start_idx end_idx\n')
		sys.exit(1)
	
	flg_header = sys.argv[1]
	merged_label = sys.argv[2]
	idx_start = int(sys.argv[3])
	idx_end = int(sys.argv[4])

	sys.stderr.write(str(idx_start)+' '+str(idx_end)+"\n")
	hd = merge_fields()
	hd.process(flg_header, merged_label, idx_start, idx_end)


	
if __name__ == '__main__':
	main()


		