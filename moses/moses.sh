#!/bin/bash

CUR_DIR=$PWD
FROM=en
TO=ru
TRAIN_FILE=../translit_ENG-RUS.train_set
TEST_FILE=../translit_ENG-RUS.test_set
MOSES_DIR=/opt/mosesdecoder
GIZA_DIR=/opt/mosesdecoder/tools
export IRSTLM=/opt/irstlm

mkdir output
./convert.py $TRAIN_FILE $FROM $TO
./convert_test_data.py $TEST_FILE $FROM $TO

mkdir lm
cd lm/
$IRSTLM/bin/add-start-end.sh < ../output/translit_$FROM-$TO.$TO > \
    translit_$FROM-$TO.sb.$TO
$IRSTLM/bin/build-lm.sh -i translit_$FROM-$TO.sb.$TO -t ./tmp \
    -p -s improved-kneser-ney -o translit_$FROM-$TO.lm.$TO
$IRSTLM/bin/compile-lm --text translit_$FROM-$TO.lm.$TO.gz \
    translit_$FROM-$TO.arpa.$TO
$MOSES_DIR/bin/build_binary translit_$FROM-$TO.arpa.$TO \
    translit_$FROM-$TO.blm.$TO

cd ..
mkdir working
cd working/
$MOSES_DIR/scripts/training/train-model.perl -root-dir \
    train_$FROM-$TO -corpus ../output/translit_$FROM-$TO -f $FROM -e \
    $TO -alignment grow-diag-final-and -reordering msd-bidirectional-fe -lm \
    0:3:$CUR_DIR/lm/translit_$FROM-$TO.blm\.$TO:8 -external-bin-dir \
    $GIZA_DIR >& training_$FROM-$TO.out

cd ..
$MOSES_DIR/bin/moses -f working/train_$FROM-$TO/model/moses.ini \
    < output/translit_$FROM-$TO.test.$FROM > output/out_$FROM-$TO.$TO
