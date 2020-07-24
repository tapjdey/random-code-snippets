#! /usr/bin/python3
"""
Run this script with ./GHminer.py <repo name> <github OAuth token>
Saves each commit json object in separate lines in a .gz file
"""
import requests, sys, re, time, datetime, json, gzip


def wait (left, headers):
  while (left < 20):
    l = requests .get('https://api.github.com/rate_limit', headers=headers)
    if (l.ok):
      left = int (l.headers.get ('X-RateLimit-Remaining'))
      reset = int (l.headers.get ('x-ratelimit-reset'))
      now = int (time.time ())
      dif = reset - now
      if (dif > 0 and left < 20):
        sys.stderr.write ("waiting for " + str (dif) + "s until"+str(left)+"s\n")
        time .sleep (dif)
    time .sleep (0.5)
  return left  


def get(url, gleft, headers, outfile, linkflag = 0):
	gleft = wait(gleft, headers)
	retry = []
	r = requests .get (url, headers=headers)
	time.sleep(0.1)
	if r.ok :
		gleft = int(r.headers.get ('X-RateLimit-Remaining'))
		links = r.headers.get ('Link')
		try:
			rj = r.json()
			for com in rj:
				outfile.write(json.dumps(com))
				outfile.write('\n')
			fail =[]
		except Exception as e:
			sys.stderr.write('Error in JSON --- '+str(e)+'\n')
			fail = [url]
		# Collecting other commits from link
		if linkflag or links is None: 
			return fail
		else:
			links = links.split(',')[1]
			part = links.split(';')
			if 'last' in part[1]:
				lastseg = part[0].split('=')
				newurl = lastseg[0].replace('<','')
				newurl = newurl.strip()
				last = int(lastseg[1].strip('>'))

				for i in range(2,last+1):
					print ('On Page',i, 'of', last)
					fail = get(newurl+'='+str(i), gleft, headers, outfile, 1)
					retry += fail
				return  retry
			else:
				return fail
	else:
		sys.stderr.write('Connection Error --- '+str(url)+'\n')
		return [url]


def main(repo,  token):
	baseurl = 'https://api.github.com/repos/'
	headers = {'Accept': 'application/vnd.github.v3+json', 'Authorization':'token ' + token}
	gleft = 0
	param = '/commits'
	# Save data
	outfile = gzip.open('commit_data_'+repo.replace('/','_')+'.gz', 'wt', encoding = 'ISO-8859-1')
	retry = get (baseurl+repo+param, gleft, headers, outfile)
	# Retry once
	if len(retry) > 0:
		for url in retry:
			get(url, gleft, headers, outfile, 1)

	outfile.close()
	
		



if __name__ == '__main__':
	if len (sys.argv) < 3:
		print ('Run with all Required Parameters')
		exit(1)
	else:
		repo = sys.argv[1]
		token = sys.argv[2]
		main(repo, token)
