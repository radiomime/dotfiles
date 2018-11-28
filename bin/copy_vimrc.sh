csplit ~/.vimrc '/^" PLUGIN VIMRC CONTENT$/' '{*}'

rm ../conf/vimrc
rm ../conf/vimrc_plugin

mv xx00 ../conf/vimrc
mv xx01 ../conf/vimrc_plugin
