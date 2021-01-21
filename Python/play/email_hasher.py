# Run as python3 <email_hasher.py <input file> <output file> <field to convert to hash in the csv - optional>
# FS etc. changed in code

import hashlib, gzip, sys

def hasher(string):
    return str(hashlib.sha1(string.encode()).hexdigest())

def main():
    of = sys.argv[2]
    inf = sys.argv[1]
    try:
        fld = int(sys.argv[3])
    except:
        fld = 0.1
    newfile = gzip.open(of, 'wt')
    with gzip.open(inf,'rt', encoding = 'latin-1') as f:
        for line in f:
            line = (line.strip())
            parts = line.split(';')
            if fld == 0.1:
            	hashed = ';'.join([hasher(x) for x in parts])
            else:
                for i in range(len(parts)):
                   if i == fld: parts[i] = hasher(parts[i])
                hashed = ';'.join(parts)
            newfile.write(hashed+'\n')

    newfile.close()

if __name__ == '__main__':
    main()
