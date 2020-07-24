import hashlib, gzip

'''Convert Author ID to SHA '''

def hasher(string):
    return str(hashlib.sha1(string.encode()).hexdigest())

def main():
    newfile = gzip.open('ghtNE2aQ.forMLF.hashed.gz', 'wt', encoding = 'latin-1')
    with gzip.open('ghtNE2aQ.forMLF2.gz','rt', encoding = 'latin-1') as f:
        for line in f:
            line = (line.strip()).replace('#','@')
            parts = line.split(';')
            hashed = ';'.join([hasher(x) if i == 4 or i == 5 else x for i,x in enumerate(parts)])
            newfile.write(hashed+'\n')
            
    newfile.close()
            
if __name__ == '__main__':
    main()
