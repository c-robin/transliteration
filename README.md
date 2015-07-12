# DSS project

The goal of this project is to be able to automatically transliterate words from one language to another. In particular, we focus on the Spanish-Portuguese and English-Russian language pairs. A first approach that we are trying is to use substitution rules, of the form: ción -> ção.

A definition of transliteration: [http://en.wikipedia.org/wiki/Transliteration](http://en.wikipedia.org/wiki/Transliteration).

## Installation

You need to install some stuff:

Python 3: 

    sudo apt-get install python3

Levenshtein library for python 3 ([https://pypi.python.org/pypi/python-Levenshtein/0.11.1/](https://pypi.python.org/pypi/python-Levenshtein/0.11.1/)):

    cd python-Levenshtein-0.11.1
    sudo python3 setup.py install

## Run the code

To generate rules (please don't overwrite rules.txt):

    ./rules.py confidence support length rules2.txt

To test these rules:

    cat rules2.txt | ./model.py

Or directly:

    ./rules.py confidence support length | ./model.py

Baseline, with only a few rules that were manually crafted:

    cat rules.txt | ./model.py

##Other leads

Use giza++ ([http://sourceforge.net/projects/mgizapp/](http://sourceforge.net/projects/mgizapp/)) to align the letters. Then use a HMM model or statistical translation to do the transliteration.
    Learn a transducer, using a RPNI-like algorithm (e.g. OSTIA). 

##Bibliography

A few (seemingly) interesting reads:

Kevin Knight and Jonathan Graehl. Machine transliteration. Computational Linguistics, 1998. (About Japanese to English phonetic transcription, not really transliteration.)

Yaser Al-Onaizan and Kevin Knight. Machine Transliteration of Names in Arabic Text. SEMITIC '02, 2002. (More interesting, because it is a spelling-based approach.)

Jong-Hoon Oh, Key-Sun Choi, and Hitoshi Isahara. A comparison of different machine transliteration models. J. Artif. Int. Res., 2006.

Anil Kumar Singh, Sethuramalingam Subramaniam, and Taraka Rama. Transliteration as alignment vs. transliteration as generation for crosslingual information retrieval. TAL, 2010. 
