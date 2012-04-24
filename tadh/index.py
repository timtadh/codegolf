import collections, os, re, sys, json, timeit, time

from tst.suffix import SuffixTree
from tst import TST

stop = {'a', 'an', 'the', 'their', 'my', 'me', 'mine', 'my', 'i', 'am', 'but',
        'is', "isn't", 'was', "wasn't"}

index = SuffixTree()
reviews = dict()
results = dict()

def clean(text):
  return (
    text
    .lower()
    .replace('/', '')
    .replace('(', '')
    .replace(')', '')
    .replace(':', '')
    .replace('.', '')
    .replace(',', '')
    .replace(';', '')
    .replace(';', '')
    .replace('?', ' ?')
    .replace('!', ' !')
    .replace('-', ' - '))

def index_review(revid, review):
  revid = revid.strip()
  text = clean(review.strip().lower())
  reviews[revid] = (id, text)
  for word in set(text.split())-stop:
    revs = index.get(word, set())
    if not revs:
      revs.add(revid)
      index[word] = revs
    else:
      revs.add(revid)

def mkindex(fname):
  print fname
  with open(fname, 'r') as f:
    for i, line in enumerate(f):
      #if i > 100: break
      if i % 100 == 0: 
        print i
        sys.stdout.flush()
      revid, review = line.split(':', 1)
      index_review(revid, review)

def query(*substrs):
  ssres = [re.compile('.{0,35}%s.{0,35}'%substr.replace('?', '\?')) for substr in substrs]
  def f_index():
    for substr in substrs:
      list(index.find(substr))
  def f_brute():
    for substr in substrs:
      [text.find(substr) for id, text in reviews.values()]

  #import pdb
  #pdb.set_trace()

  #print timeit.timeit(f_index, number=10)
  #print timeit.timeit(f_brute, number=10)
  
  sets = [set() for substr in substrs]
  for i,substr in enumerate(substrs):
    for word, revids in index.find(substr):
      sets[i] |= revids
  revids = sets[0]
  for rvs in sets[1:]:
    revids &= rvs
  revids = [revid.decode('utf8') for revid in revids]
  results[' '.join(substrs).decode('utf8')] = revids
  print json.dumps(revids)

def main():
  mkindex(sys.argv[1])
  print len(reviews)
  #sys.stderr.write('repeater.py: starting\n')
  sys.stdout.flush()
  while True:
    sys.stdout.write('> '); sys.stdout.flush()
    try: inpt = sys.stdin.readline()
    except: break;
    #if inpt is None: break;
    if not inpt:
      continue
    inpt = clean(inpt)
    #sys.stdout.write(inpt)
    #sys.stdout.flush()
    inpt = inpt.split()
    query(*inpt)
    sys.stdout.flush()
  time.sleep(1)
  print 'finished'
  #print >>sys.stderr, results
  with open('results.json', 'w') as f:
    json.dump(results, f)

if __name__ == '__main__':
  main()
 
