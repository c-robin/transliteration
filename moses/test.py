#!/usr/bin/python3
import re, sys

input_lang = sys.argv[1]
output_lang = sys.argv[2]

suffix = (input_lang, output_lang, output_lang)

with open('output/out_%s-%s.%s' % suffix) as result_file:
    results = [line[:-1].strip() for line in result_file.readlines()]

with open('output/translit_%s-%s.test.%s' % suffix) as gt_file:
    gt = [line[:-1].split(';') for line in gt_file.readlines()]

ok = 0
for i in range(len(results)):
    if results[i] in gt[i]:
        ok += 1

print(ok / len(results))
