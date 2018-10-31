#!/bin/bash

RED='\033[0;31m'
NC='\033[0m'

fix_mac_bash() {
    echo "Updating MacOS Bash shell..."
    unamestr=`uname`
    if [[ "$unamestr" == 'Darwin' ]]; then
        brew install bash
        chsh -s /usr/local/bin/bash
        sudo bash -c 'echo /usr/local/bin/bash >> /etc/shells'
        ln -s /usr/local/bin/bash /usr/local/bin/bash-terminal-app
    fi
}

setup_vim_plugins () {
    mkdir -p ~/.vim/autoload
    mkdir -p ~/.vim/bundle
    cp ../conf/autoload/* ~/.vim/autoload/
    # Better syntax highlighting
    git clone https://github.com/sheerun/vim-polyglot ~/.vim/bundle/vim-polyglot
    # Color theme
    git clone https://github.com/dikiaap/minimalist ~/.vim/bundle/minimalist
    # File Finder Plugin ( :F to search files )
    git clone https://github.com/junegunn/fzf.git ~/.vim/bundle/fzf
    git clone https://github.com/junegunn/fzf.vim.git ~/.vim/bundle/fzf-vim

    # Lightline install
    git clone https://github.com/itchyny/lightline.vim ~/.vim/bundle/lightline.vim

    # TagBar, Ctrl t to open
    git clone https://github.com/majutsushi/tagbar.git ~/.vim/bundle/tagbar

    # Auto close brackets
    git clone https://github.com/jiangmiao/auto-pairs.git ~/.vim/bundle/auto-pairs

    # Surround ( ys and then any text object to add )
    git clone https://github.com/tpope/vim-surround.git ~/.vim/bundle/vim-surround

    # Use dot commands for plugin files
    git clone https://github.com/tpope/vim-repeat.git ~/.vim/bundle/vim-repeat

    # Relative line plugin, toggle numbers w/ F1
    git clone https://github.com/ericbn/vim-relativize.git ~/.vim/bundle/vim-relativize

    # Peekabo for registers
    git clone https://github.com/junegunn/vim-peekaboo.git ~/.vim/bundle/vim-peekaboo

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

functions () {
    cp ../conf/functions ~/.functions
}

aliases () {
    cp ../conf/public_aliases ~/.public_aliases
}

function eslint () {
  if which node > /dev/null
    then
        npm install -g eslint
    else
        echo -e "${RED}Please Install NPM and run again for NPM Linter..${NC}"
    fi
}

function ctags () {
    platform='unknown'
    unamestr=`uname`
    if [[ "$unamestr" == 'Linux' ]]; then
    platform='linux'
    elif [[ "$unamestr" == 'Darwin' ]]; then
    platform='mac'
    fi

    if [[ $platform == 'mac' ]]; then
        brew install ctags
    else
        sudo apt-get install ctags
    fi
}

function powerline () {
    if which pip3 > /dev/null; then
        pip3 install --user powerline-status
        pip3 install --user powerline-gitstatus
        cp ../conf/bash_profile ~/.bash_profile
        git clone https://github.com/powerline/fonts.git --depth=1
        cd fonts
        ./install.sh
        cd ..
        rm -rf fonts
    fi
}

function python_lint () {
  if which pip3 > /dev/null
    then
        sudo -H pip3 install flake8 autopep8
    elif which pip > /dev/null
    then
        sudo -H pip install flake8 autopep8
    else
        echo -e "${RED}Please Install pip or pip3 and run again for Python Linter..${NC}"
    fi
}

install_linter () {
    setup_linter_config
    git clone https://github.com/w0rp/ale.git ~/.vim/bundle/ale
    eslint
    python_lint
}


bash && functions && aliases && tmux && setup_vim && setup_vim_plugins && ctags && powerline && fix_mac_bash


if [[ $1 = "-a" ]]; then
    echo -e "${RED}Adding Linter and Powerline to install.${NC}"
    install_linter
    powerline
else
    echo -e "${RED}No linter or powerline installed."
fi
