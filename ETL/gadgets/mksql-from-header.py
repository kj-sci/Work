# -*- coding: utf-8 -*-

import sys
import re

write = sys.stdout.write

class mksql_from_header:
	def __init__(self, table_name, loaddata_fname, schema_name):
		self.indelim = '\t'
		self.outdelim = '\t'
		self.eol = '\n'
		
		self.incode = 'cp932'
		self.outcode = 'cp932'
		
		self.table_name = table_name
		self.loaddata_fname = loaddata_fname
		self.schema_name = schema_name
		self.delimiter_data = '\\t'

	def process(self):
		fname_ctable = 'ctable_'+self.table_name+'.txt'
		fname_sqlldr = 'load_'+self.table_name+'.ctl'
		
		
		self.get_setting()

		self.num_fields_data = 0
				
		# get field info
		self.field_info = []
		for line in sys.stdin:
			line_u = unicode(line, self.incode)
			data = line[:-1].split(self.indelim)
			#data = line_u[:-1].split(self.indelim)
			self.field_info.append(data)
			
			self.num_fields_data += 1

		# set idx
		idx_data_type = self.field_name2loc['DATATYPE']
		idx_max_data_len = self.field_name2loc['MAX_DATA_LENGTH']
		if 'MIN_DATA_LENGTH' in self.field_name2loc.keys():
			idx_min_data_len = self.field_name2loc['MIN_DATA_LENGTH']
		else:
			idx_min_data_len = None
		idx_format = self.field_name2loc['FORMAT']
		
		self.idx_field_name = 2
		# Create Table
		fp_ctable = open(fname_ctable, 'w')
		fp_ctable.write('create table '+self.schema_name+'.'+self.table_name+' (\n')
		# SQLLDR
		fp_sqlldr = open(fname_sqlldr, 'w')
		fp_sqlldr.write('load data\n')
		fp_sqlldr.write("infile '"+self.loaddata_fname+"'\n")
		fp_sqlldr.write('into table '+self.schema_name+'.'+self.table_name+'\n')
		fp_sqlldr.write('append\n')
		fp_sqlldr.write("fields terminated by '"+self.delimiter_data+"'\n")
		fp_sqlldr.write('trailing nullcols\n')
		fp_sqlldr.write('(\n')
		
		for idx in range(self.num_fields_data):
			ptr = self.field_info[idx]

			field_name = ptr[self.idx_field_name]
			data_type = ptr[idx_data_type]
			max_data_len = ptr[idx_max_data_len]
			format = None
			if data_type == 'char':
				if idx_min_data_len is not None and max_data_len == ptr[idx_min_data_len]:
					data_type = 'CHAR'
				else:
					data_type = 'VARCHAR2'
				if int(max_data_len) > 255:
					format = 'CHAR('+max_data_len+')'
				data_type = data_type + '(' + max_data_len + ')'
			elif data_type == 'date':
				data_type = 'DATE'
				format = '"to_date(:'+field_name+', '+"'"+ ptr[idx_format]+"')"+'"'
			elif data_type == 'number':
				data_type = 'NUMBER' + '(' + max_data_len + ')'
			
			# write to ctable
			fp_ctable.write(field_name+' '+data_type)
			if idx < self.num_fields_data-1:
				fp_ctable.write(',')
			fp_ctable.write('\n')
			
			# write to sqlldr
			fp_sqlldr.write(field_name)
			if format is not None:
				fp_sqlldr.write(' '+format)
			if idx < self.num_fields_data-1:
				fp_sqlldr.write(',')
			fp_sqlldr.write('\n')
		
		fp_ctable.write(')\n')
		fp_sqlldr.write(')\n')
		
		#self.output_map(self.setting)
		#self.output_map(self.field_name2loc)
		#for idx in range(self.num_fields_data):
		#	self.output_array(self.field_info[idx])


		fp_ctable.close()
		fp_sqlldr.close()
		
	def get_setting(self):
		self.field_name2loc = {}
		self.setting = {}
		
		flg = 0
		while flg == 0:
			line = sys.stdin.readline()
			if line[0] != '#':
				self.field_name_header = line[:-1].split('\t')
				self.num_fields_header = len(self.field_name_header)
				for idx in range(self.num_fields_header):
					self.field_name2loc[self.field_name_header[idx]] = idx
				flg = 1
			else:
				data = line[:-1].split('\t')
				key = data[0][1:]
				value = data[1]
				self.setting[key] = value
		return
		
	def output_map(self, map_data):
		write("------------------ Map Data -----------------------------------\n")
		for key, value in map_data.items():
			write(str(key)+': '+str(value)+'\n')
		write("---------------------------------------------------------------\n")

	def output_array(self, array_data):
		write("------------------ Array Data -----------------------------------\n")
		for idx in range(len(array_data)):
			write(str(idx)+': '+str(array_data[idx])+'\n')
		write("---------------------------------------------------------------\n")
		

	

def main():
	if len(sys.argv) < 3:
		sys.stderr.write('Usage: cat datafile | python $0 tname loaddata_fname[schema] > statfile\n')
		sys.exit(1)
	
	table_name = sys.argv[1]
	loaddata_fname = sys.argv[2]
	if len(sys.argv) >= 4:
		schema_name = sys.argv[3]
	else:
		schema_name = 'tmp'
	
	hd = mksql_from_header(table_name, loaddata_fname, schema_name)
	hd.process()


	
if __name__ == '__main__':
	main()


		