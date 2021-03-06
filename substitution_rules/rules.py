#!/usr/bin/python3
from utils import *
from collections import defaultdict
import random, sys

SPA_TRAIN = '../translit_SPA-POR.train_set'

def support(pattern, data):
    """
    Returns the number of times a given rule pattern occurs in the given data
    set.
    """
    return len([word for (word, _) in data if pattern in word])

def best_confidence(pattern, alignments):
    """
    Finds the rule associated with this pattern, which has the best confidence.
    For example, for the pattern 'itis', returns rule 'ite'.
    """
    bad = 0
    rules = defaultdict(int)
    for alignment in alignments:
        for left, right in get_rules(alignment, pattern):
            if left != pattern:
                bad += 1
            else:
                rules[right] += 1

    best_score = 0
    best_rule = 0
    total = bad
    for rule, score in rules.items():
        total += score
        if score > best_score and rule != pattern:
            best_score = score
            best_rule = rule
    best_score /= total
    
    return (best_rule, best_score)

def candidate_gen(alignment):
    """
    Generates a set of candidate rule patterns for a given alignment.
    For example [('#lacta', '#lacta'), ('ncia', 'ção'), ('#', '#')] gives
    ['ncia', 'ancia', 'ncia#', 'ancia#', ...]
    """
    word = ''.join([s for (s, p) in alignment])
    indices = []
    i = 0
    for (s, p) in alignment:
        if s != p:
            indices.append((i, i + len(s)))
        i += len(s)

    candidates = []
    for (i, j) in indices:
        for k in range(max(i - 2, 0), i + 1):
            for l in range(j, min(len(word) + 1, j + 3)):
                candidates.append(word[k:l])

    return candidates

def get_rules(alignment, pattern):
    """
    Given an alignment and a pattern, returns the possible matches (right side
    of the rule). For example: [('#dod', '#dod'), ('o', 'ó'), ('#', '#')] and
    the pattern 'do' would give ['do', 'dó']
    """
    word = ''.join([s for (s, p) in alignment])
    return [get_rule(index, alignment, pattern) for index in indices(word,
        pattern)]
    
def get_rule(index, alignment, pattern):
    """
    Given an alignment and a pattern, returns the right side of the rule at a
    given index.
    For example: [('#dod', '#dod'), ('o', 'ó'), ('#', '#')] with the pattern
    'do' and the index 3, would give 'dó'
    """
    right, left = '', ''
    i = 0
    for (s, p) in alignment:
        if index >= i + len(s):
            pass
        elif index + len(pattern) <= i:
            break
        elif s == p:
            right += p[max(0, index - i):(index - i + len(pattern))]
            left += s[max(0, index - i):(index - i + len(pattern))]
        else:
            right += p
            left += s

        i += len(s)

    return (left, right)

def find_rules(alignments, min_confidence, min_support, min_length):
    """
    Given a set of alignments, returns the list of substitution rules with
    confidence above the min_confidence threshold, and support above the
    min_support threshold.
    """
    rules = dict()
    seen_candidates = set()

    for alignment in alignments:
        print(alignment)
        candidates = candidate_gen(alignment)
        for pattern in candidates:
            # No need to check a pattern that has already been checked.
            if len(pattern) < min_length or pattern in seen_candidates:
                continue
            seen_candidates.add(pattern)

            sup = support(pattern, training_data)
            # Check the support first, avoids a good deal of computation.
            if sup < min_support:
                continue

            right, conf = best_confidence(pattern, alignments)
           
            if conf < min_confidence:
                continue
            
            rules[pattern] = (right, sup, conf)
   
    return rules

def prune(rules):
    return [rule for rule in rules if keep_rule(rule, rules)]

def keep_rule(rule, rules):
    l1, r1 = rule
    for l2, r2 in rules:
        if l1 != l2 and l2 in l1 and r2 in r1:
            if l1.replace(l2, '') == r1.replace(r2, ''):
                return False
    return True

if __name__ == '__main__':
    if len(sys.argv) < 4:
        sys.exit('Usage: %s confidence support length [output]' % sys.argv[0])

    min_confidence = float(sys.argv[1])
    min_support = int(sys.argv[2])
    min_length = int(sys.argv[3])
    
    if len(sys.argv) >= 5:
        output = open(sys.argv[4], 'w')
    else:
        output = sys.stdout

    training_data = data(SPA_TRAIN)
    als = alignments(training_data)

    rules = find_rules(als, min_confidence, min_support, min_length)
    output.write('%%conf=%.2f, sup=%d, len=%d\n' % (min_confidence, min_support,
        min_length))
    
    # Apply more specific rules before more general ones (order by length)
    rules = sorted(rules.items(), key=lambda x: len(x[0]), reverse=True)
    rules = [(l, r) for (l, (r, s, c)) in rules]
    #random.shuffle(rules)

    for left, right in rules:
        output.write('%s->%s\n' % (left, right))
    
    output.close()

