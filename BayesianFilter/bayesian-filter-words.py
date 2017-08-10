#!/usr/bin/env python

import sys
import naivebayes


def main():
	if len(sys.argv) < 3:
		sys.stderr.write('Usage: python bayesian-fileter-words.py training_filename test_filename > output\n')
		sys.exit(1)
		
	nb = naivebayes.NaiveBayes()
	nb.training(sys.argv[1])
	nb.test_posterior(sys.argv[2])
	
if __name__ == "__main__":
	main()

