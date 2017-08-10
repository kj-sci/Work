# -*- coding: utf-8 -*-

import sys
import re
import os
import datetime
import time

write = sys.stdout.write

class process_files:
	def __init__(self, base_dir, max_depth):
		self.base_dir = base_dir	
		self.max_depth = max_depth
		self.target_file_pattern = '^IMG_.*\.JPG'
		self.base_cmd = 'C:\\ProgramData\\Anaconda3\\python.exe C:\\Users\\kfehvb1\\Documents\\Docs\\programs\\python\\Image\\pretty-moon-data.py'
		
	def process(self):
		self.do_process_files(self.base_dir, 0)
		
	def do_process_files(self, this_dir, this_depth):
		if this_depth > self.max_depth:
			sys.stderr.write('Skip: '+this_dir+'\n')
			return
		
		if os.path.isfile('stop.txt'):
			sys.stderr.write('Stop found. Exiting...\n')
			
		file_list = os.listdir(this_dir)
		for this_file in file_list:
			this_file_fullpath = this_dir + '\\' + this_file
			m = re.search(self.target_file_pattern, this_file)
			if m is not None:
				# process this file
				sys.stderr.write('Process '+this_file+'\n')
				self.do_command_1(this_dir, this_file)
				self.do_command_2(this_dir, this_file)
				continue
				
			if os.path.isdir(this_file_fullpath):
				self.do_process_files(this_file_fullpath, this_depth+1)
	
	def do_command_1(self, dir_name, fname_in0):
		fname_out0 = re.sub('IMG', 'MON', fname_in0)
		fname_out0 = re.sub('JPG', 'BMP', fname_out0)
		fname_in = dir_name + '\\' + fname_in0
		fname_out = dir_name + '\\' + fname_out0
		self.cmd = self.base_cmd + ' ' + fname_in + ' ' + fname_out

		#write(self.cmd+'\n')
		os.system(self.cmd)

	def do_command_2(self, dir_name, fname_in0):
		
		fname_in = dir_name + '\\' + fname_in0

		# unixtime?
		created = os.stat(fname_in).st_ctime
		last_modified = os.stat(fname_in).st_mtime
		accessed = os.stat(fname_in).st_atime
		#mtime = time.mktime((2009, 1, 2, 3, 4, 5, 0, 0, -1))

		'''
		created_dt = datetime.datetime.fromtimestamp(created)
		last_modified_dt = datetime.datetime.fromtimestamp(last_modified)
		accessed_dt = datetime.datetime.fromtimestamp(accessed)
		print('created:')
		print(created_dt)
		print('last_modified:')
		print(last_modified_dt)
		print('accessed:')
		print(accessed_dt)
		'''
		
		fname_out0 = re.sub('IMG', 'MON', fname_in0)
		fname_out0 = re.sub('JPG', 'BMP', fname_out0)
		fname_out = dir_name + '\\' + fname_out0

		os.utime(fname_out, (created, last_modified))
		
		return
	
def main():
	if len(sys.argv) < 3:
		sys.stderr.write('Usage: python $0 base_dir max_depth\n')
		sys.exit(1)
	
	base_dir = sys.argv[1]
	max_depth = int(sys.argv[2])
	
	hd = process_files(base_dir, max_depth)
	hd.process()


	
if __name__ == '__main__':
	main()


		