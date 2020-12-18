#!/bin/bash

git clone https://github.com/moses-smt/mosesdecoder

pv $1 | \
  python remove_non_utf8_chars.py | \
  python pre_cleanup.py | \
  perl ./mosesdecoder/scripts/tokenizer/normalize-punctuation.perl en | \
  perl ./mosesdecoder/scripts/tokenizer/replace-unicode-punctuation.perl | \
  perl ./mosesdecoder/scripts/tokenizer/remove-non-printing-char.perl | \
  python align_punctuation.py | \
  perl ./mosesdecoder/scripts/tokenizer/tokenizer.perl -threads 4 -no-escape -l en | \
  gawk '{print tolower($0);}' | \
  python post_cleanup.py > $2

