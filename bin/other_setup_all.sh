#!/bin/bash
mkdir ~/.vim 2>/dev/null
mkdir ~/.vim/colors
cp ../conf/*.vim ~/.vim/colors
cp ../conf/vimrc ~/.vimrc
cp ../conf/tmux.conf ~/.tmux.conf
cp ../conf/bashrc ~/.bashrc

