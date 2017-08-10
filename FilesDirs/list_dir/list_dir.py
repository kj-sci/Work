# -*- coding: utf-8 -*-

import sys
import os
import datetime

write = sys.stdout.write

class list_dir:
	def __init__(self, base_dir, max_depth):
		self.base_dir = base_dir	
		self.max_depth = max_depth
		
	def process(self):
		self.do_list_dir(self.base_dir, 0)
		
	def do_list_dir(self, this_dir, this_depth):
		if this_depth > self.max_depth:
			sys.stderr.write('Skip: '+this_dir+'\n')
			return
			
		file_list = os.listdir(this_dir)
		for this_file in file_list:
			this_file_fullpath = this_dir + '\\' + this_file
			last_modified = datetime.datetime.fromtimestamp(os.stat(this_file_fullpath).st_mtime).strftime("%Y/%m/%d")
			
			for loop in range(this_depth):
				write(' ')
			write(this_file_fullpath)
			write(' ('+last_modified+')')
			write('\n')
			if os.path.isfile(this_file_fullpath):
				pass
			elif os.path.isdir(this_file_fullpath):
				self.do_list_dir(this_file_fullpath, this_depth+1)
	
	
def main():
	if len(sys.argv) < 3:
		sys.stderr.write('Usage: python $0 base_dir max_depth\n')
		sys.exit(1)
	
	base_dir = sys.argv[1]
	max_depth = int(sys.argv[2])
	
	hd = list_dir(base_dir, max_depth)
	hd.process()


	
if __name__ == '__main__':
	main()


		