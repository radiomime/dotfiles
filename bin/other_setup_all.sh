#!/bin/bash

setup_vim_plugins () {
    mkdir -p ~/.vim/autoload
    mkdir -p ~/.vim/bundle
    cp ../conf/autoload/* ~/.vim/autoload/
    git clone https://github.com/sheerun/vim-polyglot ~/.vim/bundle/vim-polyglot
    git clone https://github.com/dikiaap/minimalist ~/.vim/bundle/minimalist
    git clone https://github.com/w0rp/ale.git ~/.vim/bundle/ale
}

setup_vim () {
    rm -rf ~/.vim
    mkdir -p ~/.vim 2>/dev/null
    mkdir -p ~/.vim/colors
    cp ../conf/vim_colors/*.vim ~/.vim/colors
    cp ../conf/vimrc ~/.vimrc
}

setup_linter_config () {
    cp ../conf/linters/.* ~/
    cp ../conf/linters/.config/* ~/.config/
}

tmux () {
    cp ../conf/tmux.conf ~/.tmux.conf
}

vim () {
    cp ../conf/bashrc ~/.bashrc
}

install_linter () {
	unamestr=`uname`
	if [[ "$unamestr" == 'Linux' ]]; then
        installer='sudo apt-get install'
	elif [[ "$unamestr" == 'Darwin' ]]; then
		installer='brew install'
	fi
    $installer eslint autopep8 flake8 -y
}

setup_vim && setup_vim_plugins && setup_linter_config && install_linter && vim && tmux
