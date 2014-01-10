#!/usr/bin/python3
import re, sys

filename = sys.argv[1]
input_lang = sys.argv[2]
output_lang = sys.argv[3]

en_filename = 'output/translit_%s-%s.%s' % (input_lang, output_lang, input_lang)
ru_filename = 'output/translit_%s-%s.%s' % (input_lang, output_lang,
        output_lang)

en_file = open(en_filename, 'w')
ru_file = open(ru_filename, 'w')

lines = open(filename).readlines()
for line in lines:
    en, ru = re.findall('#(.*?)#', line)
    en_file.write(' '.join(en) + '\n')
    ru_file.write(' '.join(ru) + '\n')

en_file.close()
ru_file.close()
