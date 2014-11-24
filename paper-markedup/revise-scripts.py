import os

original_path = '../paper-prereview/'

edit_path = '../paper-postreview/'

marked_path = '../paper-markedup/'

names = ['paper.tex', 'appendices.tex', 'conclusions.tex', 'intro.tex', 'methods.tex', 'results.tex']


for fname in names:
	cmd = '/Users/daviddarmon/Documents/Reference/L/latex/latexdiff/latexdiff {}{} {}{} > {}{}'.format(original_path, fname, edit_path, fname, marked_path, fname)
	
	os.system(cmd)