a=1
for i in *.jpg; do
  new=$(printf "%d.jpg" "$a") #04 pad to length of 4
  mv -i -- "$i" "$new"
  mv -i -- "/app/data/device/crop/$i" "/app/data/crop/$new"
  let a=a+1
done

for f in *.jpg; do
    mkdir -p "./${f%.*}";
    mv -n "$f" "./${f%.*}/2_${f}";
    mv -n "/app/data/device/crop/$f" "./${f%.*}";
done