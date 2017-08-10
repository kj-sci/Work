#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import re

write = sys.stdout.write

class mecab:
	def __init__(self):
		# 32 bit env.
		self.mecab = "C:\\Program Files\\MeCab\\bin\\mecab.exe"
		self.mecabrc = ""
		#self.mecabrc = "" #"-r C:\\Users\\KFEHVB1\\Documents\\programs\\NLP\\Mecab\\mecabrc"
		self.tmp_fname = "mecab-tmp.txt"
		
		# 64 bit env.
		#self.mecab = "C:\\Program Files (x86)\\MeCab\\bin\\mecab.exe"
		#self.mecabrc = "-r E:\\NLP\\MeCab\\mecabrc"

		self.mecab_option = ""; #"-N2"
		
		target_form = {}
		target_form[u'助詞'] = -1
		target_form[u'助動詞'] =-1
		target_form[u'連体詞'] = -1
		target_form[u'接頭詞'] = -1
		target_form[u'記号'] =-1
		target_form[u'副詞'] =-1
		target_form[u'接続詞'] =-1
		target_form[u'名詞'] = 0
		target_form[u'代名詞'] = -1
		target_form[u'固有名詞'] =0
		target_form[u'数'] =-1
		target_form[u'接尾'] =-1
		target_form[u'非自立'] =-1
		target_form[u'動詞'] = 0

		self.target_form = target_form


	def parse(self, sentence):
		#os.system(cmd)
		
		fp = open(self.tmp_fname, 'w')
		fp.write(sentence.encode('cp932'))
		fp.close()
		
		#self.cmd = "echo "+self.sentence+" | \""+self.mecab+"\" "+self.mecab_option+" "+self.mecabrc+" "
		self.cmd = "type "+self.tmp_fname+" | \""+self.mecab+"\""

		#print "==== in mecab.parse ========="
		#print "cmd: ", self.cmd
		#print "---------------------------"

		pp = os.popen(self.cmd, 'r')
		parse_result = []
		for line in pp:
			#print "============================="
			#print line
			if re.match('^EOS', line):
				continue
			data = line[:-1].split()
			if len(data) < 2:
				return None
			result = data[1].split(',')
			result.insert(0, data[0])
			parse_result.append(result)
		self.result = parse_result

	def is_target_form(self, term, idx):
		form_u = unicode(term[idx], 'cp932')
		if self.target_form.has_key(form_u) == False:
			return 1
		else:
			flg = self.target_form[form_u]
			if flg == 0:
				return self.is_target_form(term, idx+1)
			else:
				return flg

	def get_result(self):
		return self.result

	def print_result(self):
		cnt = 0
		print "------- in mecab.print_result -----------"
		for res in self.result:
			print cnt,":", res[0],":",
			for res1 in res:
				print res1+"|",
			print ''
			cnt += 1
		print "-----------------"

		
def main():
	if len(sys.argv) > 3:
		idx_id = int(sys.argv[1])
		idx_class = int(sys.argv[2])
		idx_txt = int(sys.argv[3])
	else:
		sys.stderr.write("Usage: cat datafile | python mecab.py idx_id idx_class idx_txt > output\n")
		sys.exit(1)
		
	handler = mecab()
	header = sys.stdin.readline()
		
	loop=0
	for line in sys.stdin:
		line_u = unicode(line, 'cp932')
		data = line_u[:-1].split('\t')
		num_fields = len(data)
		
		#print "################", loop, ": ", '|'.join(data), "################"
		#print "################", loop, "################"

		sentence = data[idx_txt].strip()		
		handler.parse(sentence)
		result = handler.get_result()
		#print "----------------------------------------------"
		#handler.print_result()
		
		#for i in range(num_fields):
		#	write(data[i])
		#	write('\t')
		#write("\n")
		#write("-----------------------------\n")
		
		for res in result:
			flg = handler.is_target_form(res, 1)

			#if flg < 0:
			#	continue

			write(data[idx_id].encode('cp932'))
			write('\t')
			write(data[idx_class].encode('cp932'))
			write('\t')
			write(res[0])
			write('\t')
			write(str(flg))
			write('\t')
			write(res[1])
			write('\t')
			write(res[2])
			write('\n')

			#if len(res) >= 8:
				#print '\t'.join(data[0:4]) + '\t' + '|'.join(res[0:3]) + '\t' + res[7]
			#else:
				#print '\t'.join(data[0:4]) + '\t' + '\t'.join(res[0:3]) + '\t' + ''

		#print '--------------------------------------------'
		#handler.print_result()
		
		#if loop > 10:
		#	break
		loop += 1

if __name__ == "__main__":
	main()
