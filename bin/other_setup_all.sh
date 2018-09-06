#!/bin/bash
mkdir -p ~/.vim 2>/dev/null
mkdir -p ~/.vim/colors
mkdir -p ~/.vim/autoload
mkdir -p ~/.vim/bundle
cp ../conf/autoload* ~/.vim/autoload/
git clone https://github.com/sheerun/vim-polyglot ~/.vim/bundle/vim-polyglot
cp ../conf/vim_colors/*.vim ~/.vim/colors
cp ../conf/vimrc ~/.vimrc
cp ../conf/tmux.conf ~/.tmux.conf
cp ../conf/bashrc ~/.bashrc

