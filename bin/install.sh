#!/bin/bash

setup_vim_plugins () {
    mkdir -p ~/.vim/autoload
    mkdir -p ~/.vim/bundle
    cp ../conf/autoload/* ~/.vim/autoload/
    git clone https://github.com/sheerun/vim-polyglot ~/.vim/bundle/vim-polyglot
    git clone https://github.com/dikiaap/minimalist ~/.vim/bundle/minimalist
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

bash () {
    cp ../conf/bashrc ~/.bashrc
}

install_linter () {
    setup_linter_config
    git clone https://github.com/w0rp/ale.git ~/.vim/bundle/ale
	unamestr=`uname`
	if [[ "$unamestr" == 'Linux' ]]; then
        installer='sudo apt-get install'
	elif [[ "$unamestr" == 'Darwin' ]]; then
		installer='brew install'
	fi
    $installer eslint autopep8 flake8 -y
}


bash && tmux && setup_vim && setup_vim_plugins 

RED='\033[0;31m'
NC='\033[0m' 

if [[ $1 = "-l" ]]; then
    echo -e "${RED}Adding Linter to install.${NC}"
    install_linter
else
    echo -e "${RED}No Linter installed. run with -l flag to install linter."
fi


