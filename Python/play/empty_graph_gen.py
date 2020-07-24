import re
s = '"Release.Date","New.Users","Exceptions","Usage.Intensity","Release.Duration","Usage.Frequency"'

s = re.sub(r'\"','',s)
n = s.split(',')

empty = ''
for i in n:
	empty += '['+i+']'
	
print empty

full = ''
d = []
for i in n:
	d.append(i)
	k = list(set(n) - set(d))
	full += '['+i+'|'
	for j in k:
		full += j+':'
	full = full[:-1] + ']'	
	
	
print full
