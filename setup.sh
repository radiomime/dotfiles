#!/bin/bash

sudo add-apt-repository ppa:deadsnakes/ppa
sudo add-apt-repository ppa:jonathonf/vim
sudo apt-get update
sudo apt-get install -y python3.6 vim

curl -fLo ~/.vim/autoload/plug.vim --create-dirs \
        https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim
