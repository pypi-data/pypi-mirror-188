from jft.directory.make import f as mkdirine
from jft.directory.remove import f as rmdir
from jft.file.load import f as load
from jft.file.save import f as save

data = '\n'.join([
  "__pycache__",
  "*.html",
  "*.pkl",
  "*.pickle",
  "*.xlsx",
  "*.secret",
  "functions.txt",
  "refactor.recommendations",
  "temp",
  "scrap.py",
  "skrap.py",
  "*.json",
  "history.txt",
])

f = lambda root='./': save(root + '.gitignore', data)

if __name__ == '__main__': f()

up = lambda: mkdirine('./temp/')  
dn = lambda: rmdir('./temp/')

def t():
  up()
  f('./temp/')
  result = data==load('./temp/.gitignore')
  dn()
  return result
