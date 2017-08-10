#!/usr/bin/env python
# -*- coding: utf-8 -*-

from numpy import *

class levenshteindistance:
	def __init__(self):
		self.len1 = 0
		self.len2 = 0

	def calc_distance(self, str1, str2):
		len1 = len(str1)
		len2 = len(str2)
		
		if len1 > 0 and len2 > 0:
			avg_len = (float(len1) + float(len2)) / 2.0
			return self.calc(str1, str2) / avg_len
		else:
			return 100
	
	def calc(self, str1, str2):
		self.str1 = str1
		self.str2 = str2
		self.len1 = len(str1)
		self.len2 = len(str2)
		self.edit_mat = zeros((self.len1+1, self.len2+1))
		self.docalc()

		return self.edit_mat[self.len1][self.len2]

	def docalc(self):
		for i in range(self.len1+1):
			self.edit_mat[i][0] = i
		for i in range(self.len2+1):
			self.edit_mat[0][i] = i

		for i1 in range(1, self.len1+1):
			for i2 in range(1, self.len2+1):
				#print i1, ", ", i2
				if self.str1[i1-1] == self.str2[i2-1]:
					cost = 0
				else:
					cost = 1
				
				if self.edit_mat[i1-1, i2] < self.edit_mat[i1, i2-1]:
					this_dist = self.edit_mat[i1-1, i2] + 1
				else:
					this_dist = self.edit_mat[i1, i2-1] + 1
				if this_dist > self.edit_mat[i1-1, i2-1]+cost:
					this_dist = self.edit_mat[i1-1, i2-1]+cost

				self.edit_mat[i1, i2] = this_dist

	def print_words(self):
		print self.str1, ": ", self.len1
		print self.str2, ": ", self.len2

	def print_dist_matrix(self):
		print "  ",
		for i1 in range(self.len2+1):
			print " ", i1,
		print
		for i1 in range(self.len1+1):
			print i1, " ",
			for i2 in range(self.len2+1):
				print self.edit_mat[i1][i2],
			print
		
def main():
	#str1 = u'株式会社ソニー'
	#str2 = u'（株）ソニー'
	str1 = 'kitten'
	str2 = 'sitting'

	dist_handler = levenshteindistance()
	distance = dist_handler.calc(str1, str2)

	print "-----------------------------------"
	dist_handler.print_words();
	print "-----------------------------------"
	dist_handler.print_dist_matrix();
	print "-----------------------------------"

	print "distance = ", distance



if __name__ == '__main__':
	main()
	
	