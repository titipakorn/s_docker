temp_path = "/app/data/crop/"
mkdir -p "$temp_path"
device_path = "/app/data/device/crop/" 
app_path = "/app/data/app/crop/" 
a=1
for i in *.jpg; do
  new=$(printf "%d.jpg" "$a") #04 pad to length of 4
  mv -i -- "$i" "$new"
  let a=a+1
  mv -i -- "${device_path}$i" "${temp_path}$new"
done

for j in "${device_path}"*/     # or use: subdirectory*/
do
    new=$(printf "%d.jpg" "$a") #04 pad to length of 4
    mv -i -- "$i" "${app_path}$new"
    let a=a+1
done

for f in *.jpg; do
    mkdir -p "./${f%.*}";
    mv -n "$f" "./${f%.*}/2_${f}";
    mv -n "${temp_path}$f" "./${f%.*}";
done