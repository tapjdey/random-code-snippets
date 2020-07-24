#! /usr/bin/python3
"""
Run this script with ./GHminer.py <file name with users> <github OAuth token>
Saves each issue json object in separate lines in a .gz file
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
			for com in rj['items']:
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
				newurl = "=".join(lastseg[0:-1]).replace('<','')
				newurl = newurl.strip()
				last = int(lastseg[-1].strip('>'))
				# print (newurl)
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


def main(usrfile,  token):
	baseurl = 'https://api.github.com/search/issues?q=is:pr+author:'
	headers = {'Accept': 'application/vnd.github.v3+json', 'Authorization':'token ' + token}
	gleft = 0
	with open(usrfile) as f:
		users = f.readlines()

	# Save data
	outfile = gzip.open('issue_from_'+usrfile+'.gz', 'wt', encoding = 'ISO-8859-1')
	for user in users:
		user = user.strip()
		_ =	get (baseurl+user, gleft, headers, outfile)
	

	outfile.close()
	
		



if __name__ == '__main__':
	if len (sys.argv) < 3:
		print ('Run with all Required Parameters')
		exit(1)
	else:
		usrfile = sys.argv[1]
		token = sys.argv[2]
		main(usrfile, token)
