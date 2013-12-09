#!/usr/bin/python3
from utils import *
from collections import defaultdict

SPA_TRAIN = 'translit_SPA-POR.train_set'
CONFIDENCE = 0.8
SUPPORT = 4

# Returns the number of times a given rule pattern occurs in the given data set.
def support(pattern, data):
    return len([s for (s, p) in data if pattern in s])

# Finds the rule associated with this pattern, which has the best confidence.
# For example, for the pattern 'itis', returns rule 'ite'.
def best_confidence(pattern, alignments):
    
    rules = defaultdict(int)
    for al in alignments:
        for m in matches(al, pattern):
            rules[m] += 1

    best_score = 0
    best_rule = 0
    total = 0
    for rule, score in rules.items():
        total += score
        if score > best_score and rule != pattern:
            best_score = score
            best_rule = rule
    best_score /= total
  
    # Temporary hack (a bit overkill, we probably miss many rules).
    # Some bad rules such as 'iti->ite' have a good confidence.
    # Because the match function, given [('it', 'it'), ('is', 'e'), ('#', '#')]
    # and the pattern 'iti', returns 'ite'. Thus, the confidence of 'iti->ite'
    # and 'itis->ite' is almost the same.
    # To avoid this problem, We compute the confidence of the rule in both
    # directions (Spanish->Portuguese, Portuguese->Spanish).
    if best_score >= CONFIDENCE:
        inv_score = 0
        inv_alignments = ([(p,s) for (s,p) in l] for l in alignments)
        inv_total = 0
        for al in inv_alignments:
            for m in matches(al, best_rule):
                if m == pattern:
                    inv_score += 1
                inv_total += 1
        inv_score /= inv_total
        #print('>%s->%s (%f,%f)' % (pattern, best_rule, best_score, inv_score))
        best_score = 0.5*best_score + 0.5*inv_score

    return (best_rule, best_score)

# Generates a set of candidate rule patterns for a given alignment.
# For example [('#lacta', '#lacta'), ('ncia', 'ção'), ('#', '#')] gives
# ['ncia', 'ancia', 'ncia#', 'ancia#', ...]
def candidate_gen(alignment):
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

    return [c for c in candidates if len(c) > 1]

# Given an alignment and a pattern, returns the possible matches (on the other
# side of the rule).
# For example: [('#dod', '#dod'), ('o', 'ó'), ('#', '#')] and the pattern 'do'
# would give ['do', 'dó']
def matches(alignment, pattern):
    word = ''.join([s for (s, p) in alignment])
    return [match(index, alignment, pattern) for index in indices(word,
        pattern)]
    
# Given an alignment and a pattern, returns the other part of the rule at a
# given index.
# For example: [('#dod', '#dod'), ('o', 'ó'), ('#', '#')] with the pattern 'do'
# and the index 3, would give 'dó'
def match(index, alignment, pattern):
    match = ''
    i = 0
    for (s, p) in alignment:
        if index >= i + len(s):
            pass
        elif index + len(pattern) <= i:
            break
        elif s == p:
            match += p[max(0, index - i):(index - i + len(pattern))]
        #elif index + len(pattern) >= i + len(s):
        else:
            match += p #TODO improve

        i += len(s)

    return match

# Given a set of alignments, return the list of substitution rules with
# confidence above the CONFIDENCE threshold, and support above the SUPPORT
# threshold.
def find_rules(alignments):
    rules = dict()
    dided = set()

    for alignment in alignments:
        candidates = candidate_gen(alignment)
        for pattern in candidates:
            # No need to check a pattern that has already been checked.
            if pattern in dided:# or pattern[-1] != '#':
                continue
            dided.add(pattern)

            s = support(pattern, training_data)
            # Check the support first, avoids a good deal of computation.
            if s >= SUPPORT:
                rule, c = best_confidence(pattern, alignments)
                if c >= CONFIDENCE:
                    rules[pattern] = (rule, s, c)
                    print('%s->%s (%d,%f)' % (pattern, rule, s, c))

    # Eliminate too general rules
    #new_rules = dict()
    #for s, p in rules.items():
    #    if not [k for k in rules.keys() if s != k and s in k]:
    #        new_rules[s] = p

    return rules

if __name__ == '__main__':
    filename = sys.argv[1]

    training_data = data(SPA_TRAIN)
    als = alignments(training_data)

    f = open(filename, 'w')
    rules = find_rules(als)

    rules = sorted(rules.items(), key=lambda x: -x[1][2])
    for s, (p, sup, c) in rules:
        f.write('%s->%s\n' % (s, p))
    f.close()

