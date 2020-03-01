#!/bin/sh

K0=`mktemp`
K1=`mktemp`

trap "rm $K0 $K1" 0

awk -F"\t" '/Mention/ {print $2}' "$1" | sort -k 2n,2 > $K0
awk -F"\t" '/Mention/ {print $2}' "$2" | sort -k 2n,2 > $K1

diff $K0 $K1
