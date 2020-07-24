#! /usr/bin/python3
"""
This script filters commits with the word 'fix' in commit message
"""
import gzip, json, glob, sys,re
files = glob.glob('./commit_data*')
for fn in files:
	print ('Working with',fn)
	wf = (fn.replace('.gz', '.csv.gz')).replace('commit','filtered_commit')

	of = gzip.open(wf, 'wt', encoding= 'utf-8')
	with gzip.open(fn, 'rt', encoding= 'ISO-8859-1') as f:
		for line in f:
			line = line.strip()
			com = json.loads(line)
			msg = com['commit']['message']
			if re.search(r'^fix|\sfix', msg, re.I):
				sha = com['sha']
				try:
					auth_name = com['commit']['author']['name']
					auth_email = com['commit']['author']['email']
					commit_time = com['commit']['author']['date']
				except:
					auth_name = auth_email = commit_time = ''
				try:
					auth_github = com['author']['login']
				except:
					auth_github = ''
				try:
					parent_sha = ','.join(x['sha'] for x in com['parents'])
				except:
					parent_sha = ''
				outstr = ';'.join([sha, auth_name, auth_email, auth_github, commit_time, parent_sha, (msg.replace(';',',')).replace('\n',' ')])
				of.write(outstr+'\n')


