#!/usr/bin/python3
from utils import *

SPA_TRAIN = 'translit_SPA-POR.train_set'
SPA_TEST = 'translit_SPA-POR.test_set'
RUS_TRAIN = 'translit_ENG-RUS.train_set'
RUS_TEST = 'translit_ENG-RUS.test_set'

class Model:
    def __init__(self):
        pass
    def train(self, data):
        pass
    def translate(self, word):
        return word

class RulesModel(Model):
    def __init__(self, rule_file):
        lines = open(rule_file).readlines()
        
        if lines[0].startswith('%'):
            print(lines[0][1:-1])

        self.rules = [line[:-1].split('->') for line in lines if
                not line.startswith('%') and '->' in line] 
    def translate(self, word):
        for s, p in self.rules:
            word = word.replace(s, p)
        return word

training_data = data(SPA_TRAIN)
test_data = data(SPA_TEST, True)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        model = Model()
    else:
        model = RulesModel(sys.argv[1])

    total = len(test_data)
    dist_sum = 0
    ok_count = 0

    for word, translations in test_data:
        model_translation = model.translate(word)
        dist = min([distance(model_translation, translation) for translation in
            translations])

        if dist == 0:
            ok_count += 1
        
        dist_sum += dist
    
    print('accuracy: %.1f%%, average distance: %.3f' % (100 * ok_count / total,
        dist_sum / total))

"""
conf=0.80, sup=2, len=4
accuracy: 68.1%, average distance: 0.595

Baseline rules.txt:
accuracy: 58.6%, average distance: 0.755

No rules:
accuracy: 51.0%, average distance: 1.062
"""

