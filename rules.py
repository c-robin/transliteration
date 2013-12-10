#!/usr/bin/python3
from utils import *
from collections import defaultdict

SPA_TRAIN = 'translit_SPA-POR.train_set'

def support(pattern, data):
    """
    Returns the number of times a given rule pattern occurs in the given data
    set.
    """
    return len([s for (s, p) in data if pattern in s])

def best_confidence(pattern, alignments):
    """
    Finds the rule associated with this pattern, which has the best confidence.
    For example, for the pattern 'itis', returns rule 'ite'.
    """
    bad = 0
    rules = defaultdict(int)
    for al in alignments:
        for pat, mat in matches(al, pattern):
            if pat != pattern:
                bad += 1
            else:
                rules[mat] += 1

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

def matches(alignment, pattern):
    """
    Given an alignment and a pattern, returns the possible matches (on the other
    side of the rule).
    For example: [('#dod', '#dod'), ('o', 'ó'), ('#', '#')] and the pattern 'do'
    would give ['do', 'dó']
    """
    word = ''.join([s for (s, p) in alignment])
    return [match(index, alignment, pattern) for index in indices(word,
        pattern)]
    
def match(index, alignment, pattern):
    """
    Given an alignment and a pattern, returns the other part of the rule at a
    given index.
    For example: [('#dod', '#dod'), ('o', 'ó'), ('#', '#')] with the pattern
    'do' and the index 3, would give 'dó'
    """
    match, pat = '', ''
    i = 0
    for (s, p) in alignment:
        if index >= i + len(s):
            pass
        elif index + len(pattern) <= i:
            break
        elif s == p:
            match += p[max(0, index - i):(index - i + len(pattern))]
            pat += s[max(0, index - i):(index - i + len(pattern))]
        else:
            match += p
            pat += s

        i += len(s)

    return (pat, match)


def inv_confidence(rule, alignments):
    """    
    Returns the confidence of the given rule in the opposite direction (from
    Portuguese to Spanish). Might be useful to compute a 'stricter' confidence
    measure.
    """
    pattern, match = rule
    inv_score = 0
    inv_alignments = ([(p,s) for (s,p) in l] for l in alignments)
    inv_total = 0
    for al in inv_alignments:
        for (pat, mat) in matches(al, match):
            if mat == pattern:
                inv_score += 1
            inv_total += 1
    inv_score /= inv_total
    return inv_score

def find_rules(alignments, min_confidence, min_support, min_length):
    """
    Given a set of alignments, returns the list of substitution rules with
    confidence above the min_confidence threshold, and support above the
    min_support threshold.
    """
    rules = dict()
    dided = set()

    for alignment in alignments:
        candidates = candidate_gen(alignment)
        for pattern in candidates:
            # No need to check a pattern that has already been checked.
            if len(pattern) < min_length or pattern in dided:
                continue
            dided.add(pattern)

            s = support(pattern, training_data)
            # Check the support first, avoids a good deal of computation.
            if s < min_support:
                continue

            rule, c = best_confidence(pattern, alignments)
                
            if c < min_confidence:
                continue
            #c = 0.5 * c + 0.5 * inv_confidence((pattern, rule), alignments)
            #if c < min_confidence:
            #    continue

            rules[pattern] = (rule, s, c)
            #print('%s->%s (%d, %f)' % (pattern, rule, s, c))
    
    return rules

if __name__ == '__main__':
    if len(sys.argv) != 5:
        sys.exit('Usage: %s confidence support length output' % sys.argv[0])

    min_confidence = float(sys.argv[1])
    min_support = int(sys.argv[2])
    min_length = int(sys.argv[3])
    output = sys.argv[4]

    training_data = data(SPA_TRAIN)
    als = alignments(training_data)

    f = open(output, 'w')
    rules = find_rules(als, min_confidence, min_support, min_length)
    f.write('%%conf=%.2f, sup=%d, len=%d\n' % (min_confidence, min_support,
        min_length))

    # Apply more specific rules before more general ones (order by length)
    rules = sorted(rules.items(), key=lambda x: len(x[0]), reverse=True)
    for s, (p, sup, c) in rules:
        f.write('%s->%s\n' % (s, p))
    f.close()

