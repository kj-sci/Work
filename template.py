# -*- coding: utf-8 -*-

import sys
import re
import ky_vars

write = sys.stdout.write

class template:
	def __init__(self, flg_header, table_name, schema_name):
		self.ky_vars = ky_vars.ky_vars()

		self.indelim = '\t'
		self.outdelim = '\t'
		self.eol = '\n'
		
		self.incode = 'cp932'
		self.outcode = 'cp932'
		
		self.flg_header = flg_header
		self.table_name = table_name
		self.schema_name = schema_name
		
		self.num_fields = 0
		

	def process(self):
		# get header
		if self.flg_header == '1':
			header_str = unicode(sys.stdin.readline(), self.incode)
			self.field_name = header_str[:-1].split(self.indelim)
			self.num_fields = len(self.field_name)
		elif self.flg_header == '0':
			# do nothing.
			pass
		
		if self.field_name is not None:
			print '-----------------------------------'
			self.sample_output(self.field_name)
			print '-----------------------------------'

		
		# process data
		cnt = 0
		for line in sys.stdin:
			line_u = unicode(line, self.incode)
			data = line_u[:-1].split(self.indelim)
			
			if cnt == 0:
				if self.flg_header == '0':
					self.num_fields = len(data)
					self.field_name = []
					for loop in range(self.num_fields):
						self.field_name.append('Col_'+str(loop))

			for loop in range(len(data)):
				pass
				
			self.sample_output(data)
			
			cnt += 1

			if cnt % 10 == 0:
				sys.stderr.write(str(cnt)+'\n')
				break

		
			
	def sample_output(self, data):
		print "------------------------------------------------------------"
		for loop in range(len(data)):
			write('['+str(loop)+'] '+self.field_name[loop].encode(self.outcode)+': '+data[loop].encode(self.outcode))
			write(self.eol)

	
	def is_datetime(self, str):
		m = re.search('^\d{4}/\d{1,2}/\d{1,2}\s+\d{1,2}:\d{1,2}:\d{1,2}$', str)
		if m is not None:
			self.this_date_format = 'YYYY/MM/DD HH:MI:SS'
			return 'Y'
		else:
			return 'N'



	def output(self):
		ctable_fname = 'ctable_'+self.table_name+'.txt'
		fp = open(ctable_fname, 'w')
			if self.datatype[loop] == "date" or self.datatype[loop] == "datetime" or self.datatype[loop] == "date_num":
				fp.write('date')
			elif self.datatype[loop] == "number":
					fp.write('number('+str(self.maxlen[loop])+')')
			else:
				fp.write(self.datatype[loop])
		fp.close()
	

def main():
	if len(sys.argv) < 3:
		sys.stderr.write('Usage: cat datafile | python $0 1(with header)/0(without header)/header_fname tname [schema] > statfile\n')
		sys.exit(1)
	
	flg_header = sys.argv[1]
	table_name = sys.argv[2]
	if len(sys.argv) >= 4:
		schema_name = sys.argv[3]
	else:
		schema_name = 'tmp'
	
	hd = template(flg_header, table_name, schema_name)
	hd.process()


	
if __name__ == '__main__':
	main()


		