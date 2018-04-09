#!/bin/bash
mkdir -p ~/.vim 2>/dev/null
mkdir -p ~/.vim/colors
cp ../conf/vim_colors/*.vim ~/.vim/colors
cp ../conf/vimrc ~/.vimrc
cp ../conf/tmux.conf ~/.tmux.conf
cp ../conf/bashrc ~/.bashrc

