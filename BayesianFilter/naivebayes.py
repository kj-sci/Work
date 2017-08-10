# -*- coding: shift_jis -*-
import math
import sys

write = sys.stdout.write

class NaiveBayes:
	def __init__(self):
		self.vocabularies = set() # set of words
		self.wordcount = {}	   # {category : { words : (word frequency), ...}}
		self.catcount = {}		# {category : (document frequency)}

	#################################################################
	#                                                               #
	#                API                                            #
	#                                                               #
	#################################################################
	# input: 
	# 0: Document_ID
	# 1: Category_ID
	# 2: Keyword
	def training(self, fname):
		fp = open(fname, 'r')
		header = fp.readline()
		
		cnt = 0
		tmpcnt = 0
		prev_document_id = "-------"
		prev_category_id = "-------"
		
		for line in fp:
			(document_id, category_id, word) = line[:-1].split('\t')

			if prev_document_id != document_id:
				if cnt > 0:
					self.catcountup(prev_category_id)

				cnt += 1
				prev_document_id = document_id
				prev_category_id = category_id
			
				if cnt % 1000 == 0:
					sys.stderr.write("training:"+str(cnt)+"th sample\n")
			
			self.wordcountup(word, category_id)
			
		self.catcountup(prev_category_id)

	### calculate posterior probability distribution by category
	### given trained algorithm & a document (already parsed)
	### --------------------------------------------------------
	### input: word list of the doc
	### output: [Pr(cat_1|doc), Pr(cat_2|doc), ..., Pr(cat_n|doc)]
	# input: 
	# 0: Document_ID
	# 1: Keyword
	def test_posterior(self, fname):
		# calculate log(prob) by category
		sumprob = 0
		posterior = {}
		cat_cnt = len(self.catcount.keys())

		fp = open(fname, 'r')
		header = fp.readline()
		cnt = 0
		tmpcnt = 0
		prev_document_id = "-------"
		word_list = []
		for line in fp:
			(document_id, word) = line[:-1].split('\t')

			if prev_document_id != document_id:
				if cnt > 0:
					posterior = self.posterior_words(word_list)
					self.print_posterior(posterior, prev_document_id)
					word_list = []

				cnt += 1
				prev_document_id = document_id
			
				if cnt % 1000 == 0:
					sys.stderr.write("training:"+str(cnt)+"th sample\n")
			
			word_list.append(word)
		posterior = self.posterior_words(word_list)
		self.print_posterior(posterior, prev_document_id)
		
	### calculate posterior probability distribution by category
	### given trained algorithm & a document (already parsed)
	### --------------------------------------------------------
	### input: word list of the doc
	### output: [Pr(cat_1|doc), Pr(cat_2|doc), ..., Pr(cat_n|doc)]
	def posterior_words(self, word_list):
		if word_list is None:
			return None
		
		# calculate log(prob) by category
		sumprob = 0
		posterior = {}
		cnt = len(self.catcount.keys())
		
		padding = 0
		for cat in self.catcount.keys():
			scr = self.score(word_list, cat)
			padding -= scr
		padding /= cnt
		
		for cat in self.catcount.keys():
			scr = self.score(word_list, cat) + padding
			prob = math.exp(scr)
			posterior[cat] = prob
			sumprob += prob
		
		if sumprob < 0.00000001:
			return None
		
		for cat in self.catcount.keys():
			posterior[cat] /= sumprob
		
		return posterior

	def print_posterior(self, posterior, document_id):
		if posterior is not None:
			cat_list = sorted(posterior.keys(), key=lambda x: posterior[x], reverse=True)
			write(document_id)
			for cat_loop in range(5):
				write('\t')
				if cat_loop >= len(cat_list):
					write('\t')
				else:
					write(cat_list[cat_loop])
					write('\t')
					write(str(posterior[cat_list[cat_loop]]))
			write('\n')
			
	#################################################################
	#                                                               #
	#             Help Functions                                    #
	#                                                               #
	#################################################################

		
	def wordcountup(self, word, cat):
		self.wordcount.setdefault(cat, {})
		self.wordcount[cat].setdefault(word, 0)
		self.wordcount[cat][word] += 1
		self.vocabularies.add(word)

	def catcountup(self, cat):
		self.catcount.setdefault(cat, 0)
		self.catcount[cat] += 1

		
		

	#################################################################
	#                                                               #
	#                                                               #
	#                                                               #
	#################################################################
	def score(self, word_list, cat):
		score = math.log(self.priorprob(cat))
		for w in word_list:
			if w in self.vocabularies:
				score += math.log(self.wordprob(w, cat))
		return score

	def priorprob(self, cat):
		return float(self.catcount[cat]) / sum(self.catcount.values())

	def incategory(self, word, cat):
		# returns the number of occurrence in a category
		if word in self.wordcount[cat]:
			return float(self.wordcount[cat][word])
		return 0.0

	def wordprob(self, word, cat):
		# calc P(word|cat)
		prob = \
			(self.incategory(word, cat) + 1.0) / \
				  (sum(self.wordcount[cat].values()) + \
				   len(self.vocabularies) * 1.0)
		return prob
	
	def getcategorylist():
		return wordcount.keys

	#################################################################
	#                                                               #
	#               Obsolete                                        #
	#                                                               #
	#################################################################
	### based on the trained algorithm, and a document,
	### find the best matching category to this doc.
	### classifier (document already parsed)
	def classifier_words(self, word_list):
		best = None # best category
		max = -sys.maxint
		if word_list is None:
			return None
		
		# calculate log(prob) by category
		for cat in self.catcount.keys():
			prob = self.score(word_list, cat)
			if prob > max:
				max = prob
				best = cat

		return best

