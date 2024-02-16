import os

paths = os.getenv('PATH')

PYpaths = os.getenv('PYTHONPATH')

w = open('Paths.txt','w')

w.write(paths+'\n')
w.write(PYpaths)

w.close()
#print (paths)
#print (PYpaths)