# For Retrieveing Downloads for NPM packages from NPM API
# Usage: supply package names by stdin, last date as sys.argv - %Y-%m-%d
import time, requests, sys, pymongo, json, datetime

#progress bar
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
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


if (len (sys .argv) > 1): final_date = datetime.datetime.strptime(sys.argv[1] , "%Y-%m-%d")
else: 
    print('Give Final Date')
    sys.exit(-1)

# package list
pkgs = sys.stdin.read()
pkgs = pkgs.replace('"','')
pkgs = pkgs.split(',')
pkgs[-1] = pkgs[-1].rstrip()

# loop through dates, 365 at once
start_date = datetime.datetime(2015, 3, 1)
delta = datetime.timedelta(days=365)
end_date = start_date + delta
dt_range = []

while start_date < final_date:
    if end_date > final_date : end_date = final_date
    dt_range.append((start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')))
    start_date = end_date + datetime.timedelta(days=1)
    end_date = start_date + delta
    
# MongoDB setup

client = pymongo .MongoClient (host="da1.eecs.utk.edu")
db = client ['']

#popular pkgs
coll = db['']




# get data
base_url = 'https://api.npmjs.org/downloads/range/'
outstr = ''
l = len(pkgs)
i = 0
print(l)
for pkg in pkgs:
    dl = []
    i+=1
    printProgressBar(i, l, prefix = 'Progress:', suffix = 'Complete', length = 50, decimals = 2)
    for r in dt_range:
        url = base_url+r[0]+':'+r[1]+'/'+pkg
        try: r = requests.get(url)
        except: outstr += 'Timeout '+ pkg+'\n'
        
        try:
            
            result = r.content
            try:
                rj = json.loads(result.decode('utf-8', errors='ignore'))
                dl = dl + (rj['downloads'])
            except: outstr += 'DecodeError '+ pkg+'\n'
            
        except: outstr += 'BadURL '+ pkg+'\n'
    
    ent = {pkg: dl}
    # Insert to MongoDB
    coll .insert (ent, check_keys=False)
    time .sleep (0.5)
    
with open('out_dep','a') as f2:
    f2.write(outstr)
