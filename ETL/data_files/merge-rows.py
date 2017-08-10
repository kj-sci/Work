# -*- coding: utf-8 -*-

import sys
import re
import ky_vars

write = sys.stdout.write

class merge_rows:
	def __init__(self):
		self.ky_vars = ky_vars.ky_vars()
		
	def process(self, flg_header, num_keys):
		# get header
		if flg_header == '1':
			header_str = unicode(sys.stdin.readline(), self.ky_vars.incode)
			self.field_name = header_str[:-1].split(self.ky_vars.indelim)
			self.num_fields = len(self.field_name)
			for loop in range(self.num_fields):
				if loop > 0:
					write(self.ky_vars.outdelim)
				write(self.field_name[loop])
			write('\n')
			
		elif self.flg_header == '0':
			# do nothing.
			pass
		
		#if self.field_name is not None:
		#	print '-----------------------------------'
		#	self.sample_output(self.field_name)
		#	print '-----------------------------------'

		
		# process data
		prev_keys = []
		for loop in range(num_keys):
			prev_keys.append('')
			
		merged_data = []
		for loop in range(self.num_fields):
			merged_data.append('')
			
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

			flg_new = 0
			for loop in range(num_keys):
				if prev_keys[loop] != data[loop]:
					flg_new = 1
					break
					
			if flg_new == 0:
				for loop in range(num_keys, self.num_fields):
					merged_data[loop] += ' / ' + data[loop]
			else:
				if cnt > 0:
					# print data
					for loop in range(self.num_fields):
						if loop > 0:
							write(self.ky_vars.outdelim)
							
						if loop < num_keys:
							write(prev_keys[loop].encode(self.ky_vars.outcode))
						else:
							write(merged_data[loop].encode(self.ky_vars.outcode))
							merged_data[loop] = ''
					write('\n')
				
				# set merged data
				for loop in range(num_keys, self.num_fields):
					merged_data[loop] = data[loop]

				# set keys
				for loop in range(num_keys):
					prev_keys[loop] = data[loop]
				
			cnt += 1

			if cnt % 1000 == 0:
				sys.stderr.write(str(cnt)+'\n')
				#break

		# print data
		for loop in range(self.num_fields):
			if loop > 0:
				write(self.ky_vars.outdelim)
				
			if loop < num_keys:
				write(prev_keys[loop].encode(self.ky_vars.outcode))
			else:
				write(merged_data[loop].encode(self.ky_vars.outcode))
				merged_data[loop] = ''
		write('\n')
		
			
	def sample_output(self, data):
		print "------------------------------------------------------------"
		for loop in range(len(data)):
			write('['+str(loop)+'] '+self.field_name[loop].encode(self.ky_vars.outcode)+': '+data[loop].encode(self.ky_vars.outcode))
			write(self.ky_vars.eol)

	
def main():
	if len(sys.argv) < 3:
		sys.stderr.write('Usage: cat datafile | python $0 1(with header)/0(without header) num_keys\n')
		sys.exit(1)
	
	flg_header = sys.argv[1]
	num_keys = int(sys.argv[2])

	sys.stderr.write("#Keys: "+str(num_keys)+"\n")
	hd = merge_rows()
	hd.process(flg_header, num_keys)


	
if __name__ == '__main__':
	main()


		