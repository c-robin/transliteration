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
        rule_lines = open(rule_file).readlines()
        self.rules = [line[:-1].split('->') for line in rule_lines] 
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
    dist = 0
    ok = 0

    for word,translations in test_data:
        tr = model.translate(word)
        d = min([distance(tr, translation) for translation in translations])
        dist += d
        if d == 0:
            ok += 1
    
    print('accuracy: %f, average distance: %d' % (ok / total, dist))

