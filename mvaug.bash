for dir in */     # or use: subdirectory*/
do
    find "\${dir}output" -type f -name "*.jpg" -exec cp -t "\${dir}" {} +
    rm -rf "\${dir}output";
done