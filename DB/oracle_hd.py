#!/usr/bin/python

import cx_Oracle
import sys

write = sys.stdout.write

class oracle_hd:
	def __init__(self, id, pw):
		self.id = id
		self.pw = pw
	
	def process(self):
		auth = self.id + '/' + self.pw + '@orcl'
		try:
			connection = cx_Oracle.connect(auth)
			cursor = connection.cursor()
			sql = u'Select * From aiu16.dwh_duns_industry_class where rownum < 10'
			result = cursor.execute(sql)
			loop=0
			for row in result:
				for idx in range(len(row)):
					if idx > 0:
						write('\t')
					write(row[idx])
				write('\n')
			cursor.close()
			connection.close()
		#except cx_Oracle.DatabaseError, exc:
		except:
			sys.stderr.write("Error\n")

		
		
def main():
	if len(sys.argv) < 3:
		sys.stderr.write('Usage: python hd_oracle.py id pw\n')
		sys.exit(1)
	
	id = sys.argv[1]
	pw = sys.argv[2]

	hd = oracle_hd(id, pw)
	hd.process()
	

if __name__ == '__main__':
	main()
	
	