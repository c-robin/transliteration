#!/usr/bin/python3
import re, sys

_, filename, label, action = sys.argv

ext = '.test' if action == 'test' else ''
input_filename = 'output/translit_%s%s.input' % (label, ext)
output_filename = 'output/translit_%s%s.out' % (label, ext)

with open(input_filename, 'w') as input_file, open(output_filename, 'w') as output_file:
    lines = open(filename).readlines()
    for line in lines:
        words = re.findall('#(.*?)#', line)

        input_file.write(' '.join(words[0]) + '\n')

        if action == 'test':
            output_file.write(';'.join([' '.join(w) for w in words[1:]]) + '\n')
        else:
            output_file.write(' '.join(words[1]) + '\n')

