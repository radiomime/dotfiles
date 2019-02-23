#!/bin/bash

RED='\033[0;31m'
NC='\033[0m'

add_timezone() {
    if grep "TZ=" ~/.profile > /dev/null;then
        echo "Not Adding Timezone..."
    else
        echo "Adding Timezone..."
        echo "TZ='America/Denver'; export TZ" >> ~/.profile
    fi
}

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

setup_completion () {

    if ls ~/.vim/bundle/YouCompleteMe > /dev/null;then
        echo "YouCompleteMe Plugin installed."
    else
        git clone https://github.com/Valloric/YouCompleteMe ~/.vim/bundle/YouCompleteMe
        ( cd ~/.vim/bundle/YouCompleteMe ; git submodule update --init --recursive)
        unamestr=`uname`
        if [[ "$unamestr" == 'Linux' ]]; then
            sudo apt-get install build-essential cmake python-dev
        elif [[ "$unamestr" == 'Darwin' ]]; then
            brew install cmake
        fi
        ( cd ~/.vim/bundle/YouCompleteMe ; ./install.py --clang-completer )
        ( cd ~/.vim/bundle/YouCompleteMe ; sudo bash ./install.sh )

    fi
}

setup_vim_plugins () {
    cat ../conf/vimrc_plugin >> ~/.vimrc
    mkdir -p ~/.vim/autoload
    mkdir -p ~/.vim/bundle
    cp ../conf/autoload/* ~/.vim/autoload/
    # Better syntax highlighting
    if ls ~/.vim/bundle/vim-polygot > /dev/null;
    then
        echo "Polygot Vim Plugin installed."
    else
        git clone https://github.com/sheerun/vim-polyglot ~/.vim/bundle/vim-polyglot
    fi

    # Color Scheme Plugins
    if ls ~/.vim/bundle/minimalist > /dev/null;then
        echo "Minimalist Plugin installed."
    else
        git clone https://github.com/dikiaap/minimalist ~/.vim/bundle/minimalist
    fi


    if ls ~/.vim/bundle/vim-monokai-tasty > /dev/null;then
        echo "Monokai Tasty Plugin installed."
    else
        git clone https://github.com/patstockwell/vim-monokai-tasty.git ~/.vim/bundle/vim-monokai-tasty
    fi

    # File Finder Plugin ( :F to search files )
    if ls ~/.vim/bundle/fzf > /dev/null;then
        echo "Fzf Plugin installed."
    else
        git clone https://github.com/junegunn/fzf.git ~/.vim/bundle/fzf
        git clone https://github.com/junegunn/fzf.vim.git ~/.vim/bundle/fzf-vim
    fi

    # Lightline install

    if ls ~/.vim/bundle/lightline > /dev/null;then
        echo "Lightline Plugin installed."
    else
        git clone https://github.com/itchyny/lightline.vim ~/.vim/bundle/lightline.vim
    fi

    # TagBar, Ctrl t to open

    if ls ~/.vim/bundle/tagbar > /dev/null;then
        echo "Tagbar Plugin installed."
    else
        git clone https://github.com/majutsushi/tagbar.git ~/.vim/bundle/tagbar
    fi

    # Auto close brackets

    if ls ~/.vim/bundle/auto-pairs > /dev/null;then
        echo "Auto Pairs Plugin installed."
    else
        git clone https://github.com/jiangmiao/auto-pairs.git ~/.vim/bundle/auto-pairs
    fi

    # Surround ( ys and then any text object to add )

    if ls ~/.vim/bundle/vim-surround > /dev/null;then
        echo "Vim Surround Plugin installed."
    else
        git clone https://github.com/tpope/vim-surround.git ~/.vim/bundle/vim-surround
    fi

    # Use dot commands for plugin files

    if ls ~/.vim/bundle/vim-repeat > /dev/null;then
        echo "Vim Repeat Plugin installed."
    else
        git clone https://github.com/tpope/vim-repeat.git ~/.vim/bundle/vim-repeat
    fi

    # Peekabo for registers

    if ls ~/.vim/bundle/vim-peekaboo > /dev/null;then
        echo "Vim Peekaboo Plugin installed."
    else
        git clone https://github.com/junegunn/vim-peekaboo.git ~/.vim/bundle/vim-peekaboo
    fi


    if ls ~/.vim/bundle/vim-easymotion > /dev/null;then
        echo "Vim Easymotion Plugin installed."
    else
        git clone https://github.com/easymotion/vim-easymotion.git ~/.vim/bundle/vim-easymotion
    fi


    if ls ~/.vim/bundle/matchit > /dev/null;then
        echo "Vim Matchit Plugin installed."
    else
        git clone https://github.com/tmhedberg/matchit.git ~/.vim/bundle/matchit
    fi


    if ls ~/.vim/bundle/zoomwin > /dev/null;then
        echo "Vim ZoomWin Plugin installed."
    else
        git clone https://github.com/vim-scripts/ZoomWin.git ~/.vim/bundle/zoomwin
    fi

    if ls ~/.vim/bundle/goyo > /dev/null;then
        echo "Vim Goyo Plugin installed."
    else
        git clone https://github.com/junegunn/goyo.vim.git ~/.vim/bundle/goyo
    fi

    # Vim autocompletion
    setup_completion
}

setup_notes () {
    mkdir -p ~/.notes
    platform='unknown'
    unamestr=`uname`
    if [[ "$unamestr" == 'Darwin' ]]; then
        if ls ~/.vim/bundle/markdown > /dev/null;then
            echo "Markdown installed."
        else
            npm -g install instant-markdown-d
            git clone https://github.com/suan/vim-instant-markdown.git ~/.vim/bundle/markdown
        fi
    fi
}

setup_vim () {
    mkdir -p ~/.vim 2>/dev/null
    mkdir -p ~/.vim/colors
    cp ../conf/vim_colors/*.vim ~/.vim/colors
    cp ../conf/skeletons ~/.vim
    cp ../conf/vimrc ~/.vimrc
}

setup_linter_config () {
    cp ../conf/linters/.* ~/
    cp ../conf/linters/.config/* ~/.config/
}

tmux () {
    cp ../conf/tmux.conf ~/.tmux.conf
}

fzf_install () {
    cp ../conf/fzf_functions ~/.fzf_functions
    PATH=~/.bin:$PATH
    if which fzf > /dev/null; then
        echo "FZF already installed!"
    else
        git clone --depth 1 https://github.com/junegunn/fzf.git ~/.fzf
        ~/.fzf/install
    fi
}

bash () {
    cp ../conf/bashrc ~/.bashrc
    cp -r ../conf/bin ~/.bin
}

functions () {
    cp ../conf/functions ~/.functions
}

aliases () {
    cp ../conf/public_aliases ~/.public_aliases
}

eslint () {
    if which node > /dev/null
    then
        if npm show eslint > /dev/null;then
            echo "ESLint already installed";
        else
            npm install -g eslint
        fi
    else
        echo -e "${RED}Please Install NPM and run again for NPM Linter..${NC}"
    fi
}

ctags () {
    platform='unknown'
    unamestr=`uname`
    if [[ "$unamestr" == 'Linux' ]]; then
        platform='linux'
    elif [[ "$unamestr" == 'Darwin' ]]; then
        platform='mac'
    fi

    if [[ $platform == 'mac' ]]; then
        if which ctags > /dev/null;then
            echo "Ctags already installed"
        else
            brew install ctags fd
        fi
    else
        if which ctags > /dev/null; then
            echo "Ctags already installed"
        else
            sudo apt-get install ctags highlight
            wget https://github.com/sharkdp/fd/releases/download/v7.2.0/fd-musl_7.2.0_amd64.deb
            sudo dpkg -i fd-musl_7.2.0_amd64.deb
            rm fd-*
        fi
    fi
}

powerline () {
    if which pip3 > /dev/null; then
        if pip3 show powerline-status > /dev/null;then
            echo "Powerline already installed."
        else
            pip3 install --user powerline-status
            pip3 install --user powerline-gitstatus
            cp ../conf/bash_profile ~/.bash_profile
            git clone https://github.com/powerline/fonts.git --depth=1
            cd fonts
            ./install.sh
            cd ..
            pip3 show powerline-status|grep Location: | awk '{print $2}' | xargs  printf 'source %s' >> ~/.bash_profile
            printf '%s' "/powerline/bindings/bash/powerline.sh" >> ~/.bash_profile
            rm -rf fonts
        fi
    fi
}


python_lint () {
    if which pip3 > /dev/null
    then
        if pip3 show flake8 > /dev/null
        then
            echo "Flake8 already installed."
        else
            sudo -H pip3 install flake8
        fi
        if pip3 show autopep8 > /dev/null
        then
            echo "Autopep8 already installed."
        else
            sudo -H pip3 install autopep8
        fi
    elif which pip > /dev/null
    then
        sudo -H pip install flake8 autopep8
    else
        echo -e "${RED}Please Install pip or pip3 and run again for Python Linter..${NC}"
    fi
}

install_linter () {
    if ls ~/.vim/bundle/ale > /dev/null;then
        echo "Ale Plugin installed."
    else
        setup_linter_config
        git clone https://github.com/w0rp/ale.git ~/.vim/bundle/ale
        eslint
        python_lint
    fi
}

# Run the install scripts

if [[ $1 = "-l" ]]; then
    echo -e "${RED}Running lightweight install!${NC}"
    bash  && functions && aliases && tmux && setup_vim && add_timezone
else
    bash && fzf_install && functions && aliases && tmux && setup_vim && setup_vim_plugins && ctags && powerline && fix_mac_bash && add_timezone
fi

if [[ $1 = "-a" ]]; then
    echo -e "${RED}Adding Linter and Powerline to install.${NC}"
    install_linter
    powerline
    setup_notes
else
    echo -e "${RED}No linter or powerline installed."
fi
