for dir in */     # or use: subdirectory*/
do
    find "${dir}output" -not -type d -print0 | xargs -0J % mv -f % $dir ;
    rm -rf "${dir}output";
done