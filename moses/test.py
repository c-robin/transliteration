#!/usr/bin/python3
import re, sys
from Levenshtein import distance
from collections import Counter

label = sys.argv[1]

with open('output/out_%s.out' % label) as result_file:
    results = [line[:-1].strip() for line in result_file.readlines()]

with open('output/translit_%s.test.out' % label) as gt_file:
    gt = [line[:-1].split(';') for line in gt_file.readlines()]

total = len(results)
hist = []
for model_tr, translations in zip(results, gt):
    dist,translation = min([(distance(model_tr, tr), tr) for tr in translations])
    
    hist.append(dist)

    if dist >= 8:
        #print(model_tr + ' // ' + translation)
        pass

print(len(hist), total)
precision = len([x for x in hist if x==0])/total
mean = sum(hist)/total
variance = sum((x-mean)**2 for x in hist)/total 

print(Counter(hist))
print('accuracy: %.1f%%, mean: %.3f, variance: %.3f' % (100*precision, mean, variance))
