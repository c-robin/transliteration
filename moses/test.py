#!/usr/bin/python3
import re, sys

label = sys.argv[1]

with open('output/out_%s.out' % label) as result_file:
    results = [line[:-1].strip() for line in result_file.readlines()]

with open('output/translit_%s.test.out' % label) as gt_file:
    gt = [line[:-1].split(';') for line in gt_file.readlines()]

ok = 0
for i in range(len(results)):
    if results[i] in gt[i]:
        ok += 1

print(ok / len(results))
