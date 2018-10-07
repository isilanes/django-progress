cd WebProgress/templates/
rm -f main_index.html
ln -s main_index_free.html main_index.html
cd ../..

cd gasolina/
rm -f static
ln -s static-free static
cd ..
