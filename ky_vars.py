#!/usr/bin/env python
# -*- coding: utf-8 -*-

class ky_vars:
	def __init__(self):
		# orcl
		self.orcl_id = ''
		self.orcl_pw = ''
		self.orcl_tns = 'orcl'

		# win
		self.win_id = 'this_id'
		self.win_pw = ''
		self.win_proxy = 'this_id:this_port'
		
		self.indelim = '\t'
		self.outdelim = '\t'
		self.eol = '\n'
		
		self.incode = 'cp932'
		self.outcode = 'cp932'
		
		self.sleep_time = [60, 180, 300, 600, 1200, 1800, 3600]
		
		self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
		self.http_header = { 'User-Agent' : self.user_agent }
		self.http_values = {'name' : 'Michael Foord',
          'location' : 'Northampton',
          'language' : 'Python' }
		
	def get_var(self, var_name):
		if var_name == 'orcl_id':
			return self.orcl_id
		elif var_name == 'orcl_pw':
			return self.orcl_pw
		elif var_name == 'orcl_tns':
			return self.orcl_tns
		else:
			return 'NA'

	