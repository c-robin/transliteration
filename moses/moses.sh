#!/bin/bash

# Usage: ./moses.sh FILE ACTION LABEL
# FILE: training or test file
# ACTION: "train" or "test"
# LABEL: label for the output files (e.g. SPA, or ENG)

CUR_DIR=$PWD

FILE=$1
ACTION=$2
LABEL=$3

MOSES_DIR=/opt/mosesdecoder
GIZA_DIR=/opt/mosesdecoder/tools
export IRSTLM=/opt/irstlm

# Training step
if [ "$ACTION" == "train" ]; then
mkdir -p output
./convert.py $FILE $LABEL "train"

# Language model training
mkdir -p lm
cd lm/
$IRSTLM/bin/add-start-end.sh < ../output/translit_$LABEL.out > \
    translit_$LABEL.sb.out
$IRSTLM/bin/build-lm.sh -i translit_$LABEL.sb.out -t ./tmp \
    -p -s improved-kneser-ney -o translit_$LABEL.lm.out -n 3
$IRSTLM/bin/compile-lm --text translit_$LABEL.lm.out.gz \
    translit_$LABEL.arpa.out
$MOSES_DIR/bin/build_binary translit_$LABEL.arpa.out \
    translit_$LABEL.blm.out -i

# Word alignment
cd $CUR_DIR
mkdir -p working
cd working/
$MOSES_DIR/scripts/training/train-model.perl -root-dir \
    train_$LABEL -corpus ../output/translit_$LABEL -f input -e \
    out -alignment grow-diag-final -reordering monotone --max-phrase-length 3 -lm \
    0:3:$CUR_DIR/lm/translit_$LABEL.blm\.out:8 -external-bin-dir \
    $GIZA_DIR >& training_$LABEL.out 
fi

# Evaluation step
if [ "$ACTION" == "test" ]; then
./convert.py $FILE $LABEL "test"

TEST_INPUT=output/translit_$LABEL.test.input 
TEST_TRUTH=output/translit_$LABEL.test.out
TEST_OUTPUT=output/out_$LABEL.out
MODEL=working/train_$LABEL/model/moses.ini

#$MOSES_DIR/scripts/training/filter-model-given-input.pl $TEST_INPUT $MODEL $TEST_TRUTH

$MOSES_DIR/bin/moses -f $MODEL -distortion-limit 0 < $TEST_INPUT > $TEST_OUTPUT
fi
