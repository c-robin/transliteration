from Levenshtein import opcodes, distance
import re, sys

def data(filename, several_values=False):
    lines = open(filename).readlines()
    words = [re.findall('(#.*?#)', line) for line in lines]

    if several_values:
        return [(l[0], l[1:]) for l in words]
    else:
        return [(l[0], l[1]) for l in words]


def alignments(data):
    alignments = []
    for s, p in data:
        ops = opcodes(s, p)
        align = []
        word1, word2 = '', ''
        equal = True
        for op, i1, e1, i2, e2 in ops:
            if (op == 'equal' and not equal) or (op != 'equal' and equal):
                equal = (op == 'equal')
                if word1 or word2:
                    align.append((word1, word2))
                    word1, word2 = '', ''
            
            word1 += s[i1:e1]
            word2 += p[i2:e2]
        if word1 or word2:
            align.append((word1, word2))

        alignments.append(align)
    return alignments

def indices(string, pattern):
    offset = 0
    indices = []

    while string:
        try:
            index = string.index(pattern)
            string = string[index + len(pattern):]
            indices.append(offset + index)
            offset += index + len(pattern)
        except:
            break
    return indices

