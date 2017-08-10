# -*- coding: utf-8 -*-

import sys
import re

write = sys.stdout.write

class mksql_ctable:
	def __init__(self, delimiter, flg_header, header_fname, table_name, schema_name, load_file_name):
		self.indelim = delimiter
		self.outdelim = '\t'
		self.eol = '\n'
		
		self.incode = 'cp932'
		self.outcode = 'cp932'
		#self.incode = 'utf8'
		#self.outcode = 'utf8'
		
		self.flg_header = flg_header
		self.header_fname = header_fname
		
		self.table_name = table_name
		self.schema_name = schema_name
		self.load_file_name = load_file_name
		
		self.num_fields = 0
		
	def init_vars(self):
		self.maxlen = [-1]*self.num_fields
		self.minlen = [-1]*self.num_fields
		self.max_digit_len = [-1]*self.num_fields
		self.maxval = [None]*self.num_fields
		self.minval = [None]*self.num_fields
		self.num_null = [0]*self.num_fields
		self.datatype = ['']*self.num_fields
		self.date_format = ['']*self.num_fields

	def init_datatype(self):
		for loop in range(self.num_fields):
			m = re.search('_CD$', self.field_name[loop].upper())
			if m is not None:
				self.datatype[loop] = 'char'
				
			m = re.search('_CODE$', self.field_name[loop].upper())
			if m is not None:
				self.datatype[loop] = 'char'

			m = re.search('_KBN$', self.field_name[loop].upper())
			if m is not None:
				self.datatype[loop] = 'char'

			m = re.search('_KUBUN$', self.field_name[loop].upper())
			if m is not None:
				self.datatype[loop] = 'char'

			m = re.search('_TYP$', self.field_name[loop].upper())
			if m is not None:
				self.datatype[loop] = 'char'

			m = re.search('_TYPE$', self.field_name[loop].upper())
			if m is not None:
				self.datatype[loop] = 'char'

	def process(self):
		# get header
		if self.flg_header == '1':
			header_str = unicode(sys.stdin.readline(), self.incode)
			if self.header_fname == 'null':
				self.field_name = header_str[:-1].split(self.indelim)
				self.num_fields = len(self.field_name)
				self.init_vars()
				self.init_datatype()
		elif self.flg_header == '0':
			# do nothing.
			pass

		if self.header_fname != 'null':
			#temp_header_str = unicode(sys.stdin.readline(), self.incode)
			self.field_name = []
			fp = open(self.header_fname, 'r')
			self.num_fields = 0
			for line in fp:
				line_u = unicode(line, self.incode)
				#print line_u.encode(self.incode)
				item_u = line_u[:-1].split(self.indelim)
				#print ('|'.join(item_u)).encode(self.incode)
				#print "---------------------"
				self.field_name.append(item_u[0])
				self.num_fields += 1
			fp.close()
			self.init_vars()
			self.init_datatype()
		
		# process data
		cnt = 0
		cnt_warn = 0
		for line in sys.stdin:
			line_u = unicode(line, self.incode)
			data = line_u[:-1].split(self.indelim)
			
			if cnt == 0:
				if self.flg_header == '0':
					self.num_fields = len(data)
					self.init_vars()
					self.field_name = []
					for loop in range(self.num_fields):
						self.field_name.append('Col_'+str(loop))

			if len(data) > self.num_fields:
				sys.stderr.write('----------------------------------------\n')
				sys.stderr.write('WARNING in line '+str(cnt)+self.eol)
				self.sample_stderr_output(data)
				cnt_warn += 1
				if cnt_warn > 10:
					sys.exit(1)
			
			
			for loop in range(self.num_fields):
				if len(data[loop]) == 0:
					self.num_null[loop] += 1
				else:
					if len(self.datatype[loop]) == 0:
						self.datatype[loop] = self.check_datatype(data[loop], loop)
						if self.datatype[loop] == 'datetime' or self.datatype[loop] == 'date' or self.datatype[loop] == 'date_num':
							self.date_format[loop] = self.this_date_format
							
					else:
						if self.datatype[loop] == 'datetime':
							if self.is_datetime(data[loop]) == 'Y':
								pass
							elif self.is_date(data[loop]) == 'Y':
								self.datatype[loop] = 'date'
							else:
								self.datatype[loop] = 'char'
								
						elif self.datatype[loop] == 'date':
							if self.is_date(data[loop]) == 'Y':
								pass
							else:
								self.datatype[loop] = 'char'
						elif self.datatype[loop] == 'date_num':
							if self.is_date_num(data[loop]) == 'Y':
								pass
							elif self.is_number(data[loop], loop) == 'Y':
								self.datatype[loop] = 'number'
							else:
								self.datatype[loop] = 'char'
						elif self.datatype[loop] == 'number':
							if self.is_number(data[loop], loop) == 'Y':
								self.datatype[loop] = 'number'
							else:
								self.datatype[loop] = 'char'
								print "-------- number => char (loop: ", str(loop), ")-------------------------"
								self.sample_output(data)
					this_len = len(data[loop].encode(self.outcode))
					if self.maxlen[loop] == -1 or self.maxlen[loop] < this_len:
						self.maxlen[loop] = this_len
					if self.minlen[loop] == -1 or self.minlen[loop] > this_len:
						self.minlen[loop] = this_len

					try:
						if (self.datatype[loop] == 'number' or self.datatype[loop] == 'date_num') and (self.maxval[loop] is None or float(self.maxval[loop]) < float(data[loop])):
							self.maxval[loop] = data[loop]
					except:
						sys.stderr.write('ERROR:\n')
						sys.stderr.write('(line, idx) = ('+str(cnt)+', '+str(loop)+')'+self.eol)
						sys.stderr.write('data = ('+data[loop]+')'+self.eol)
						sys.stderr.write('------------------------------------------------------\n')
						sys.stderr.write(line)
						self.sample_stderr_output(data)
						sys.stderr.write('date_num: '+self.is_date_num(data[loop])+self.eol)
						sys.exit(1)
						
					if (self.datatype[loop] == 'number' or self.datatype[loop] == 'date_num') and (self.minval[loop] is None or float(self.minval[loop]) > float(data[loop])):
						self.minval[loop] = data[loop] 

			#self.sample_output(data)
			
			cnt += 1

			if cnt % 10000 == 0:
				sys.stderr.write(str(cnt)+'\n')
				#break
				
		self.total_cnt = cnt
		# output data
		self.output_stats()
		self.output_ctable()
		self.output_sqlldr()
		
			
	def sample_stderr_output(self, data):
		sys.stderr.write("------------------------------------------------------------\n")
		for loop in range(len(data)):
			sys.stderr.write('['+str(loop)+'] ')
			try:
				sys.stderr.write(self.field_name[loop].encode(self.outcode))
			except:
				sys.stderr.write('-')
			sys.stderr.write(': '+data[loop].encode(self.outcode))
			sys.stderr.write(self.outdelim)
			try:
				sys.stderr.write(self.datatype[loop])
			except:
				sys.stderr.write('-')
			sys.stderr.write(self.eol)


	def sample_output(self, data):
		print "------------------------------------------------------------"
		for loop in range(len(data)):
			write('['+str(loop)+'] '+self.field_name[loop].encode(self.outcode)+': '+data[loop].encode(self.outcode))
			if self.datatype[loop] is None:
				write(self.outdelim+'-')
			else:
				write(self.outdelim+self.datatype[loop])

			if self.minlen[loop] == -1:
				write(self.outdelim+'-')
			else:
				write(self.outdelim+str(self.minlen[loop]))

			if self.maxlen[loop] == -1:
				write(self.outdelim+'-')
			else:
				write(self.outdelim+str(self.maxlen[loop]))

			if self.minval[loop] is None:
				write(self.outdelim+'-')
			else:
				write(self.outdelim+self.minval[loop])
			if self.maxval[loop] is None:
				write(self.outdelim+'-')
			else:
				write(self.outdelim+self.maxval[loop])
			write(self.outdelim+str(self.num_null[loop]))
			write(self.outdelim+self.date_format[loop])
			
			write(self.eol)

	##### find datatype
	def check_datatype(self, str, loop):
		if self.is_datetime(str) == 'Y':
			return 'datetime'
		elif self.is_date(str) == 'Y':
			return 'date'
		elif self.is_date_num(str) == 'Y':
			return 'date_num'
		elif self.is_number(str, loop) == 'Y':
			return 'number'
		else:
			return 'char'
	
	def is_number(self, str, loop):
		if str == '0':
			return 'Y'

		m = re.search('\.(.*)$', str)
		if m is not None:
			l = len(m.group(1))
			if l > self.max_digit_len[loop]:
				self.max_digit_len[loop] = l
			
		m = re.search('^([\+\-])?[1-9][\d\.\,]*$', str)
		if m is not None:
			return 'Y'
		else:
			m = re.search('^([\+\-])?0\.[\d]*$', str)
			if m is not None:
				return 'Y'
			else:
				return 'N'
	
	def is_date_num(self, str):
		m = re.search('^\d{8,8}$', str)
		if m is not None:
			str_int = int(str)
			if str_int >= 19000101 and str_int < 29991231:
				self.this_date_format = 'YYYYMMDD'
				return 'Y'
			else:
				return 'N'
		else:
			return 'N'
	
	def is_date(self, str):
		m = re.search('^\d{4,4}\-\d{1,2}\-\d{1,2}$', str)
		if m is not None:
			self.this_date_format = 'YYYY-MM-DD'
			return 'Y'

		m = re.search('^\d{4,4}/\d{1,2}/\d{1,2}$', str)
		if m is not None:
			self.this_date_format = 'YYYY/MM/DD'
			return 'Y'
		else:
			return 'N'
		
	def is_datetime(self, str):
		m = re.search('^\d{4,4}\-\d{1,2}\-\d{1,2}\s+\d{1,2}:\d{1,2}:\d{1,2}$', str)
		if m is not None:
			self.this_date_format = 'YYYY-MM-DD HH:MI:SS'
			return 'Y'

		m = re.search('^\d{4,4}/\d{1,2}/\d{1,2}\s+\d{1,2}:\d{1,2}:\d{1,2}$', str)
		if m is not None:
			self.this_date_format = 'YYYY/MM/DD HH:MI:SS'
			return 'Y'
		else:
			return 'N'

	#### output functions
	def output_stats(self):
		print "/*******************************************************\n"
		print " *                                                     *\n"
		print " *         Stats                                       *\n"
		print " *                                                     *\n"
		print " *******************************************************/\n"
		print 'total #reocords:'+self.outdelim+str(self.total_cnt)
		print ''
		
		print "id\tlabel\tdatatype\tmax(val)\tmin(val)\tmax(len)\tmin(len)\tmax_digit_len\tnum_null\tdate_format\n"
		for loop in range(self.num_fields):
			write(str(loop))
			write(self.outdelim+self.field_name[loop].encode(self.outcode))

			if self.datatype[loop] is None:
				write(self.outdelim+'-')
			else:
				write(self.outdelim+self.datatype[loop])

			if self.maxval[loop] is None:
				write(self.outdelim+'-')
			else:
				write(self.outdelim+self.maxval[loop])
			if self.minval[loop] is None:
				write(self.outdelim+'-')
			else:
				write(self.outdelim+self.minval[loop])

			if self.maxlen[loop] == -1:
				write(self.outdelim+'-')
			else:
				write(self.outdelim+str(self.maxlen[loop]))
			if self.minlen[loop] == -1:
				write(self.outdelim+'-')
			else:
				write(self.outdelim+str(self.minlen[loop]))
			if self.max_digit_len[loop] == -1:
				write(self.outdelim+'-')
			else:
				write(self.outdelim+str(self.max_digit_len[loop]))

			write(self.outdelim+str(self.num_null[loop]))
			write(self.outdelim+self.date_format[loop])


			write(self.eol)
		write(self.eol)


	def output_ctable(self):
		## output: create table
		ctable_fname = 'ctable_'+self.table_name+'.txt'
		fp = open(ctable_fname, 'w')
		fp.write("/*******************************************************"+self.eol)
		fp.write(" *                                                     *"+self.eol)
		fp.write(" *         CREATE TABLE                                *"+self.eol)
		fp.write(" *                                                     *"+self.eol)
		fp.write(" *******************************************************/"+self.eol)
		fp.write("create table "+self.schema_name+'.'+self.table_name+" ("+self.eol)
		for loop in range(self.num_fields):
			fp.write("  "+self.field_name[loop].encode(self.outcode)+" ")

			if self.datatype[loop] == "date" or self.datatype[loop] == "datetime" or self.datatype[loop] == "date_num":
				fp.write('date')
			elif self.datatype[loop] == "char":
				if self.minlen[loop] == self.maxlen[loop]:
					fp.write('char('+str(self.maxlen[loop])+')')
				else:
					fp.write('varchar2('+str(self.maxlen[loop])+')')
			elif self.datatype[loop] == "number":
					fp.write('number('+str(self.maxlen[loop])+')')
			else:
				fp.write(self.datatype[loop])
			if loop < self.num_fields-1:
				fp.write(",")
			fp.write(self.eol)
		fp.write(')'+self.eol)
		fp.close()
	
	def output_sqlldr(self):
		## output: sqlloader
		sqlldr_fname = 'load_'+self.table_name + '.ctl'
		
		fp = open(sqlldr_fname, 'w')
		#fp.write("/*******************************************************"+self.eol)
		#fp.write(" *                                                     *"+self.eol)
		#fp.write(" *          SQL LOADER                                 *"+self.eol)
		#fp.write(" *                                                     *"+self.eol)
		#fp.write(" *******************************************************/"+self.eol)
		
		if self.flg_header == '1':
			fp.write("options(skip=1)"+self.eol)
		fp.write("load data"+self.eol)
		fp.write("infile '"+self.load_file_name+"'"+self.eol)
		fp.write("into table "+self.schema_name+'.'+self.table_name+self.eol)
		fp.write("append"+self.eol)
		fp.write("fields terminated by '\\t' trailing nullcols"+self.eol)
		fp.write("("+self.eol)
		
		for loop in range(self.num_fields):
			fp.write("  "+self.field_name[loop].encode(self.outcode))
			if self.datatype[loop] == "date" or self.datatype[loop] == "datetime" or self.datatype[loop] == "date_num":
				fp.write(" \"to_date(:"+self.field_name[loop].encode(self.outcode)+", '"+self.date_format[loop]+"')\"")
			if loop < self.num_fields-1:
				fp.write(",")
			fp.write(self.eol)
		fp.write(")"+self.eol)
		fp.close()
	
	

def main():
	if len(sys.argv) < 5:
		sys.stderr.write('Usage: cat datafile | python $0 delimiter(tab/,/etc.) 1(with header)/0(without header) header_fname(null if no header file) tname [schema] [load_fname] > statfile\n')
		sys.exit(1)
	
	delimiter = sys.argv[1]
	if delimiter == 'tab':
		delimiter = '\t'
	
	flg_header = sys.argv[2]
	header_fname = sys.argv[3]
	table_name = sys.argv[4]
	if len(sys.argv) >= 6:
		schema_name = sys.argv[5]
	else:
		schema_name = 'tmp'

	if len(sys.argv) >= 7:
		load_file_name = sys.argv[6]
	else:
		load_file_name = 'XXX'
	
	hd = mksql_ctable(delimiter, flg_header, header_fname, table_name, schema_name, load_file_name)
	hd.process()


	
if __name__ == '__main__':
	main()


		