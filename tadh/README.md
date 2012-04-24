My Solution
===========

This solution isn't really fair. It uses a Suffix Tree built on a Ternary Search
Trie (see https://github.com/timtadh/tst).

#### To use

- install https://github.com/timtadh/tst
- run `python index.py /path/to/reviews/reviews.full`

It will take 5.5 minutes to index (and use 1.2GB of memory) but it will compute
most queries really quickly (mean: `0.061`, stdev: `0.159`, 
CI(95%): `(0.032, 0.09)`).

#### What is a TST again?

see http://blog.hackthology.com/ternary-search-tries-for-fast-flexible-string

