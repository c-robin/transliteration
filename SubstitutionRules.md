#Transliteration by substitution rules

# Introduction #

Our baseline is the file `rules.txt`, which contains a few rules that we added manually.
The accuracy is: **58.6%**, and the average levenshtein distance: **0.755**

# Current approach #

Spanish and Portuguese words are close enough to use a Levenshtein distance to align their letters.

An alignement looks like this:
```
[('#aut', '#aut'), ('o', 'ó'), ('psia#', 'psia#')]
```
Using this alignment, we compute a list of candidate rule patterns:
`['o', 'to', 'op', 'top', ...]`, and for each of these patterns we compute its support (the number of times it appears in the training set), and the rule (e.g. `top -> tóp`) with the best confidence.
We keep the rules that are above a certain support threshold (for performance reasons, and to avoid overfitting), and above a confidence threshold.

The best results we obtained so far are an accuracy of **65.3%**, with an average distance of **0.638**. This is not enough, if we consider the results obtained with the baseline (we would expect at least 80%).

# Improvement ideas #

  * Improve the baseline, by adding more rules, in order to find out if the substitution rule idea could achieve fair results (are the rules are expressive enough to model the transliteration concept?).
  * Apply the more specific rules before the more general ones.
  * Limit the overlap of rule application on the same word (we don't want to modify the same zone twice).