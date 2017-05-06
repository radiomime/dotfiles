#!/bin/bash
mkdir ~/.vim 2>/dev/null
cp -r vimFolder/colors ~/.vim/colors
cp vimFolder/vimrc ~/.vimrc
cp tmux.conf ~/.tmux.conf
rm -rf ../myVim
cd ..
