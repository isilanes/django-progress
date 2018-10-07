cd WebProgress/templates/
rm -f main_index.html
ln -s main_index_nonfree.html main_index.html
cd ../..

cd gasolina/
rm -f static
ln -s static-nonfree static
cd ..
