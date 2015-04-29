import os

original_path = '../paper-for_plos/'

edit_path = '../paper-for_plos-revised/'

marked_path = '../paper-for_plos-markedup/'

names = ['paper.tex']


for fname in names:
	cmd = '/Users/daviddarmon/Documents/Reference/L/latex/latexdiff/latexdiff {}{} {}{} > {}{}'.format(original_path, fname, edit_path, fname, marked_path, fname)
	
	os.system(cmd)