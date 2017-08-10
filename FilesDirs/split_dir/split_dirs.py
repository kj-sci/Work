# -*- coding: utf-8 -*-

import sys
import re
import os
import datetime

write = sys.stdout.write

class split_dirs:
	def __init__(self, base_dir, fname_pattern):
		self.base_dir = base_dir	
		self.fname_pattern = fname_pattern
		
	def process(self):
		file_list = os.listdir(self.base_dir)
		for this_file in file_list:
			m = re.search(self.fname_pattern, this_file)
			if m is not None:
				this_file_fullpath = self.base_dir + '\\' + this_file
				last_modified = datetime.datetime.fromtimestamp(os.stat(this_file_fullpath).st_mtime).strftime("%Y%m%d")
				dir_name = self.base_dir  + '\\' + last_modified
				new_file_fullpath = dir_name + '\\' + this_file
				if not os.path.isdir(dir_name):
					# make dir
					os.mkdir(dir_name)
				# move to dir
				sys.stderr.write('mv '+this_file_fullpath+' '+new_file_fullpath+'\n')
				os.rename(this_file_fullpath, new_file_fullpath)
		
	
def main():
	if len(sys.argv) < 2:
		sys.stderr.write('Usage: python $0 base_dir\n')
		sys.exit(1)
	
	base_dir = sys.argv[1]
	fname_pattern = '^.*\.jpg'
	
	hd = split_dirs(base_dir, fname_pattern)
	hd.process()


	
if __name__ == '__main__':
	main()


		