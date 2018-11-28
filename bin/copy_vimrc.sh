csplit ~/.vimrc '/^" PLUGIN VIMRC CONTENT$/' '{*}'

file=./xx00
if [ -e "$file"  ]; then
    rm ../conf/vimrc
    mv xx00 ../conf/vimrc
else
    echo "Couldn't get first section of vimrc."
fi
file=./xx01
if [ -e "$file"  ]; then
    rm ../conf/vimrc_plugin
    mv xx01 ../conf/vimrc_plugin
else
    echo "Couldn't get plugin section of vimrc"
fi

