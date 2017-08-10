# -*- coding: utf-8 -*-

import sys
import os
import re

write = sys.stdout.write

class list_files:
	def __init__(self, base_dir, base_dir_2, max_depth):
		self.base_dir = base_dir
		self.base_dir_2 = base_dir_2
		self.max_depth = max_depth
		self.outdelim = '|'
		self.file_list = []
		
	def process(self):
		files = os.listdir(self.base_dir)
		for user_name in files:
			fullpath = self.base_dir + '\\' + user_name
			file_long = '\\' + user_name
			if os.path.isdir(fullpath):
				ftype = 'DIR'
				self.do_list_files(user_name, file_long, '', 1)
		
	def do_list_files(self, user_name, dir_name, category_name, depth):
		full_dir_name = self.base_dir + dir_name
		
		if depth >= self.max_depth:
			sys.stderr.write('Stop: '+ dir_name+'\n')
			return
			
		files = os.listdir(full_dir_name)
		loop=0
		for file in files:
			if file == 'Temp' or file == 'Obsolete':
				sys.stderr.write('Skip: '+ file+'\n')
				continue
			m = re.search('\.header$', file)
			if m is not None:
				sys.stderr.write('Skip: '+ file+'\n')
				continue
				
			fullpath = full_dir_name + '\\' + file
			file_long = dir_name + '\\' + file
			new_category_name = category_name + '/' + file
			if os.path.isdir(fullpath):
				ftype = 'DIR'
				self.do_list_files(user_name, file_long, new_category_name, depth+1)
			else:
				ftype = 'FILE'
				dummy = [user_name, category_name, file, fullpath]
				self.file_list.append(dummy)
				#print(user_name+self.outdelim+category_name+self.outdelim+file+self.outdelim+fullpath)
			loop += 1
	
	def print_data(self, out_fname):
		fp_w = open(out_fname, 'w', encoding='cp932')
		#fp_w = open(out_fname, 'w', encoding='eucjp')
		
		prev_user = ''
		prev_categ = ''
		loop = 1
		for ptr in self.file_list:
			location = '[[Folder:'+self.base_dir_2 + '/' + ptr[0] + ptr[1]+']]'
			user = ptr[0]
			
			if prev_user == ptr[0]:
				ptr[0] = '~'
				if prev_categ == ptr[1]:
					ptr[1] = '~'
					location = '~'
				else:
					prev_categ = ptr[1]
			else:
				prev_user = ptr[0]
				prev_categ = ptr[1]
				loop = 1
				
			description = re.sub('/', '_', 'SCI_DataLake_' + user + '_DAT_' + str(loop))
			if ptr[1] != '~':
				if len(ptr[1]) == 0:
					ptr[1] = '/'
				ptr[1] = '[['+ptr[1]+'>'+description+']]'
				loop += 1
		
			#print(self.outdelim+ptr[0]+self.outdelim+ptr[1]+self.outdelim+ptr[2]+self.outdelim)
			#for loop in range(4):
			#	ptr[loop] = ptr[loop].encode('euc_jp')
				
			fp_w.write(self.outdelim+ptr[0]+self.outdelim+ptr[1]+self.outdelim+location+self.outdelim+ptr[2]+self.outdelim+'\n')
		fp_w.close()
	
def main():
	if len(sys.argv) < 4:
		# folder_name: Y:\Data
		# folder_name_2: file://RKDA0201/DataLake/Data
		# output file name: result.txt
		sys.stderr.write('Usage: python $0 folder_name folder_name_2 output\n')
		sys.exit(1)
	
	base_dir = sys.argv[1]
	base_dir_2 = sys.argv[2]
	output_fname = sys.argv[3]
	max_depth = 5
	
	hd = list_files(base_dir, base_dir_2, max_depth)
	hd.process()
	hd.print_data(output_fname)


	
if __name__ == '__main__':
	main()


		