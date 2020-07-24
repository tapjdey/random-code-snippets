#! /usr/bin/python

"""
added, deleted, modified files in bot commits
"""
import sys,  yaml, json
from collections import Counter
from io import open

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 2, length = 100, fill = '%'):

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
	sys.stdout.write('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix))
	sys.stdout.flush()
	# Print New Line on Complete
	if iteration == total: 
		print ''

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

def write2file(outfile, commit, comtype, langset):
	outstr = '\n'+commit+';'+comtype+';'+','.join(list(langset))
	
	outfile.write(outstr.decode("utf-8"))
	return


def main(fn):
	langdict = get_yml()
	# statdict = {'added':Counter(), 'deleted':Counter(), 'modified':Counter()}
	
	i = 0
	l = 150632492

	outf = open('commit_lang.csv','w')
	outf.write(('Commit; Commit.Type; Languages').decode("utf-8"))
	prevcom = ''
	af = df = mf = -1
	langset = set()
	with open(fn, 'r', encoding='ISO-8859-1') as f:
		for line in f:
			i += 1
			printProgressBar(i,l)
			line = line.strip()
			parts = line.split(';')
			fl = parts[1].split('/')[-1]
			ext = fl.split('.')[-1]
			com = parts[0]
			if com != prevcom:
				if af == -1:
					pass
				elif af:
					if df:
						if mf:
							write2file(outf, prevcom, 'ADM', langset)
						else:
							write2file(outf, prevcom, 'AD', langset)
					elif mf:
						write2file(outf, prevcom, 'AM', langset)
					else:
						write2file(outf, prevcom, 'A', langset)
				elif df:
					if mf:
						write2file(outf, prevcom, 'DM', langset)
					else:
						write2file(outf, prevcom, 'D', langset)
				elif mf:
					write2file(outf, prevcom, 'M', langset)
				else:
					print 'Unknown Error',com,i
					sys.exit(1)
				af = df = mf = 0
				prevcom = com
				langset = set()
			
			try:
				lang = langdict['.'+ext]
			except:
				try:
					lang = langdict[fl]
				except:
					lang = 'Other'

			langset.add(lang)
			if ';;' in line:
				df = 1
			elif len(parts) == 3:
				af = 1
			elif len(parts) == 4:
				mf = 1
			else:
				print ('Unknown Issue', line)
				sys.exit(1)

	if af == -1:
		pass
	elif af:
		if df:
			if mf:
				write2file(outf, prevcom, 'ADM', langset)
			else:
				write2file(outf, prevcom, 'AD', langset)
		elif mf:
			write2file(outf, prevcom, 'AM', langset)
		else:
			write2file(outf, prevcom, 'A', langset)
	elif df:
		if mf:
			write2file(outf, prevcom, 'DM', langset)
		else:
			write2file(outf, prevcom, 'D', langset)
	elif mf:
		write2file(outf, prevcom, 'M', langset)

	outf.close()
	return




if __name__ == '__main__':
	fn = sys.argv[1]
	main(fn)
