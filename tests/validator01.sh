#!/bin/sh
python2 ../validator.py -f test.dat -l
echo '###'
cat test.dat | python2 ../validator.py -f test.dat -l
echo '###'
python2 ../validator.py -f test.dat -l --filter all
echo '###'
cat test.dat | python2 ../validator.py -f test.dat -l --filter all 
echo '###'
python2 ../validator.py -f test.dat -l --filter valid
echo '###'
cat test.dat | python2 ../validator.py -f test.dat -l --filter valid
echo '###'
python2 ../validator.py -f test.dat -l --filter invalid
echo '###'
cat test.dat | python2 ../validator.py -f test.dat -l --filter invalid
echo '###'
