import sys
import re
import hashlib

write = sys.stdout.write

class data_handler:
	def __init__(self):
		self.indelim = '\t'
		self.outdelim = '\t'
		self.md5_prefix = 'a1gjpn'
		
	def init(self, fld_md5, encoding):
		self.fld_md5 = fld_md5
		self.encoding = encoding
	
	def process(self, header_flg):
		cnt = 0

		# process header
		if header_flg == 'Y':
			header_str = sys.stdin.readline()
			header_str_u = unicode(header_str, self.encoding)
			self.label = header_str_u[:-1].split(self.indelim)
			num_fields = len(self.label)

			# write header
			#write(header_str)
			for loop in range(num_fields):
				if loop > 0:
					write('\t')
					
				write(self.label[loop].encode(self.encoding))
				if self.fld_md5.has_key(loop) == 1:
					write('_HEX')
			write('\n')
			cnt += 1
			
		else:
			num_fields = -1
			
		for line in sys.stdin:
			line_u = unicode(line, self.encoding)
			data = line_u[:-1].split(self.indelim)

			if cnt == 0:
				num_fields = len(data)

			for loop in range(num_fields):
				if loop > 0:
					write(self.outdelim)
				
				if self.fld_md5.has_key(loop) == 1 and len(data[loop]) > 0:
					#val = re.sub('-', '', data[loop])
					val = data[loop].encode(self.encoding)
					# check:
					#sys.stderr.write(str(loop)+": "+self.label[loop]+"=")
					#sys.stderr.write(data[loop].encode(self.encoding)+"\n")
					
					m = hashlib.md5()
					m.update(self.md5_prefix)
					m.update(val)
					data[loop] = m.hexdigest()[:16]
					#data[loop] = data[loop] + '###' + val
					
				write(data[loop].encode(self.encoding))
			write("\n")
			cnt += 1
			if cnt % 10000 == 0:
				sys.stderr.write(str(cnt)+"\n")
				

def str2dict(str, val):
	dict = {}

	if len(str) == 0:
		return dict

	str_list = str.split(',')

	for l in str_list:
		dict[int(l)] = val
	
	return dict
	
def main():
	if len(sys.argv) < 3:
		sys.stderr.write("Usage: type datafile | python mask-md5.py header_flg(Y/N) fields_to_md5(csv) > output\n")
		sys.exit(1)

	# set header flg
	header_flg = sys.argv[1]

	# set fields to md5
	fld_md5_str = sys.argv[2]
	fld_md5 = str2dict(fld_md5_str, 1)

	# encoding: cp932
	encoding = 'cp932'

	hd = data_handler()
	hd.init(fld_md5, encoding)

	hd.process(header_flg)

if __name__ == '__main__':
	main()



