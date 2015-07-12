## Resources ##

  * Moses' website: http://www.statmt.org/moses/
  * Moses' manual: http://www.statmt.org/moses/manual/manual.pdf

Even though the manual seems quite thick (about 300 pages), the installation steps are _relatively_ straightforward.

Follow the section `2.1 Getting Started with Moses`, for the installation instructions, and `2.2 Baseline System`, for the building of a translation system using Moses (example on French to English translation).

## Results ##

On the English-Russian corpus, we get a score of `BLEU = 31.33, 92.5/85.1/80.7/77.0 (BP=0.375, ratio=0.505, hyp_len=11738, ref_len=23263)`, and an accuracy of 59.1%.

On the Spanish-Portuguese corpus, we get a score of `BLEU = 41.83, 95.8/90.1/85.6/80.8 (BP=0.476, ratio=0.574, hyp_len=11874, ref_len=20690)`, and an accuracy of 56.1%.