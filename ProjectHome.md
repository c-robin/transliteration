# DSS project #
The goal of this project is to be able to automatically transliterate words from one language to another. In particular, we focus on the Spanish-Portuguese and English-Russian language pairs.
A first approach that we are trying is to use substitution rules, of the form: `ción -> ção`.

A definition of transliteration: http://en.wikipedia.org/wiki/Transliteration.

## Installation ##
You need to install some stuff:
  * Python 3: `sudo apt-get install python3`
  * Levenshtein library for python 3 (https://pypi.python.org/pypi/python-Levenshtein/0.11.1/):
```
cd python-Levenshtein-0.11.1
sudo python3 setup.py install
```

## Run the code ##
To generate rules (please don't overwrite rules.txt):
`./rules.py confidence support length rules2.txt`

To test these rules:
`cat rules2.txt | ./model.py`

Or directly:
`./rules.py confidence support length | ./model.py`

Baseline, with only a few rules that were manually crafted:
`cat rules.txt | ./model.py`

## Other leads ##
  * Use giza++ (http://sourceforge.net/projects/mgizapp/) to align the letters. Then use a HMM model or statistical translation to do the transliteration.
  * Learn a transducer, using a RPNI-like algorithm (e.g. OSTIA).

## Bibliography ##
A few (seemingly) interesting reads:
  * Kevin Knight and Jonathan Graehl. _[Machine transliteration](http://acl.ldc.upenn.edu/J/J98/J98-4003.pdf)_. Computational Linguistics, 1998. (About Japanese to English phonetic transcription, not really transliteration.)
  * Yaser Al-Onaizan and Kevin Knight. _[Machine Transliteration of Names in Arabic Text](http://aclweb.org/anthology//W/W02/W02-0505.pdf)_. SEMITIC '02, 2002. (More interesting, because it is a spelling-based approach.)
  * Jong-Hoon Oh, Key-Sun Choi, and Hitoshi Isahara. _[A comparison of different machine transliteration models](http://www.jair.org/media/1999/live-1999-2886-jair.pdf)_. J. Artif. Int. Res., 2006.
  * Anil Kumar Singh, Sethuramalingam Subramaniam, and Taraka Rama. _[Transliteration as alignment vs. transliteration as generation for crosslingual information retrieval](http://www.atala.org/IMG/pdf/5-Sight-TAL51-2.pdf)_. TAL, 2010.