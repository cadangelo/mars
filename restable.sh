#!/bin/bash
file="$1"
filename=$(basename $file .lis)
grep -E 'Tot. response' $file > res.txt
grep -E 'Detector n:' $file > det.txt
awk '{$1=""; $2=""; gsub(/\dt/,""); print}' det.txt > det2.txt
awk '{$1=""; $2=""; $3=""; $5=""; print}' res.txt > res2.txt
paste det2.txt res2.txt | column -s $'\t' -t > "$filename.txt"
sed -i '/0.000000/d' "$filename.txt"
rm res.txt
rm det.txt
rm res2.txt
rm det2.txt
