#! /usr/bin/python

"""
list if files modified by a bot
"""
import sys,  yaml, json, gzip
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '%'):
	"""
	Call in a loop to create terminal progress bar
	@params:
	    iteration   - Required  : current iteration (Int)
	    total       - Required  : total iterations (Int)
	    prefix      - Optional  : prefix string (Str)
	    suffix      - Optional  : suffix string (Str)
	    decimals    - Optional  : positive number of decimals in percent complete (Int)
	    length      - Optional  : character length of bar (Int)
	    fill        - Optional  : bar fill character (Str)
	"""
	percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
	filledLength = int(length * iteration // total)
	bar = fill * filledLength + '-' * (length - filledLength)
	print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
	# Print New Line on Complete
	if iteration == total: 
		print()

def get_yml():
	with open('./rough/languages.yml', 'r') as f:
		d = yaml.safe_load(f)
	
	langdict = {}
	for key in d:
		try:
			for ext in d[key]['extensions']:
				if ext not in langdict.keys():
					langdict[ext] = key
				else:
					langdict[ext] = langdict[ext]+';'+key
		except:
			pass
		try:
			for fl in d[key]['filenames']:
				if fl not in langdict.keys():
					langdict[fl] = key
				else:
					langdict[fl] = langdict[fl] +';'+key

		except:
			pass
	return langdict

def main(infile):
	of = open('bot_files','w', encoding='latin-1')
	langdict = get_yml()
	l = 13762430
	i = 0
	with gzip.open(infile, 'rt', encoding='latin-1') as f:
		prevbot = ''
		botfile = set()
		for line in f:
			printProgressBar(i,l)
			i+=1
			parts = (line.strip()).split(';')
			bot  = parts[0]
			if bot != prevbot:
				if prevbot == '':
					prevbot = bot
				else:
					outstr = prevbot+';'+';'.join(list(botfile))+'\n'
					of.write(outstr)
					prevbot = bot
					botfile = set()
			files = parts[4].split(',')
			for foo in files:
				foo = foo.split('/')[-1]
				ext = foo.split('.')[-1]
				try:
					lang = langdict['.'+ext]
				except:
					try:
						lang = langdict[foo]
				    except:
				    	lang = 'Other'
				botfile.add(lang)
		outstr = prevbot+';'+';'.join(list(botfile))+'\n'
		of.write(outstr)
	of.close()
	return


if __name__ =='__main__':
	infile = sys.argv[1]
	main(infile)
