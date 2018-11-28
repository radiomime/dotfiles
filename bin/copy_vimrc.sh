csplit ~/.vimrc '/^" PLUGIN VIMRC CONTENT$/' '{*}'
mv xx00 ../conf/vimrc
mv xx01 ../conf/vimrc_plugin
