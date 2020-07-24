#! /usr/bin/python3
"""
Run this script with ./PRparse.py <file name with issues json> <github OAuth token>
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
		try:
			rj = r.json()
			prj = '_'.join((rj['url'].replace('https://api.github.com/repos/','')).split('/')[:2])

			outfile.write(rj['user']['login']+';'+ prj+';'+ rj['created_at']+';'+str(rj['merged']))
			outfile.write('\n')

		except Exception as e:
			sys.stderr.write('Error in JSON --- '+str(e)+'\n')

		
	else:
		sys.stderr.write('Connection Error --- '+str(url)+'\n')
	return gleft



def main(usrfile,  token):
	headers = {'Accept': 'application/vnd.github.v3+json', 'Authorization':'token ' + token}
	gleft = 0
	outfile = gzip.open('PR_from_'+usrfile+'.gz', 'wt', encoding = 'ISO-8859-1')
	with gzip.open(usrfile, 'rt') as f:
		for line in f:
			issue_obj = json.loads(line.strip())
			prurl = issue_obj['pull_request']['url']
			gleft = get (prurl, gleft, headers, outfile)
	

	outfile.close()
	
		



if __name__ == '__main__':
	if len (sys.argv) < 3:
		print ('Run with all Required Parameters')
		exit(1)
	else:
		usrfile = sys.argv[1]
		token = sys.argv[2]
		main(usrfile, token)
