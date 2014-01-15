#!/usr/bin/python3
from utils import *
from pprint import pprint

SPA_TRAIN = 'predicted.txt'
SPA_TEST = '../translit_ENG-RUS.test_set'

training_data = data_one(SPA_TRAIN)
test_data = data(SPA_TEST, True)

#model = RulesModel(sys.stdin)

total = len(test_data)
dist_sum = 0
ok_count = 0
i=0

for word, translations in test_data:
    model_translation = training_data[i]
    pprint(model_translation)
    pprint(translations)
    dist,translation = min([(distance(model_translation, tr), tr) for tr in translations])
    i=i+1
    if model_translation == translation:
        ok_count += 1
    dist_sum += dist

print('accuracy: %.1f%%, average distance: %.3f' % (100 * ok_count / total, dist_sum / total))


