from git import Repo
import distutils
from colorama import init
from termcolor import colored
import re
import sys
from sys import platform
from os.path import expanduser
import os

init()


def cp(src, dst):
    os.system("cp -r " + src + " " + dst)


def add_user(file):
    return file.replace("~", expanduser("~"))


PLUGIN_PATH = add_user("~/.vim/bundle/")


def append(file, text):
    open(add_user(file), "a+")\
        .write(text)


def has_word(word, file):
    for line in open(add_user(file)).readlines():
        if re.search(word, line):
            return True

    return False


def is_mac():
    if platform.lower() == "darwin":
        return True

    return False


def is_linux():
    if platform.lower() == "linux":
        return True

    return False


def is_plugin(file):
    if os.path.isdir(PLUGIN_PATH + file):
        return True
    return False

# Install functions


def fix_mac_bash():
    # Update Mac Bash shell

    if is_mac():
        os.system("brew install bash")
        os.system("chsh -s /usr/local/bin/bash")
        os.system("sudo bash -c 'echo /usr/local/bin/bash >> /etc/shells'")
        os.system("ln -s /usr/local/bin/bash /usr/local/bin/bash-terminal-app")


def append_plugin_vimrc():
    os.system("cp ../conf/vimrc " + add_user("~/.vimrc"))

    fin = open("../conf/vimrc_plugin", "r")
    data2 = fin.read()
    fin.close()
    fout = open(add_user("~/.vimrc"), "a")
    fout.write(data2)
    fout.close()


cp_files = {
    "../conf/bashrc": "~/.bashrc",
    "../conf/bin": "~/.bin",
    "../conf/functions": "~/.functions",
    "../conf/public_aliases": "~/.public_aliases",
    "../conf/tmux.conf": "~/.tmux.conf",
    "../conf/vim_colors/*.vim": "~/.vim/colors",
    "../conf/autoload/*": "~/.vim/autoload/",
    "../conf/skeletons": "~/.vim",
    "../conf/vimrc": "~/.vimrc",
    "../conf/linters/.*": "~/",
    "../conf/linters/.config/*": "~/.config/"
}


def setup_plugins(plugin_list):
    append_plugin_vimrc()
    for plugin in plugin_list:
        for repo in plugin['git']:
            name = git_extract_name(repo)
            if(is_plugin(name)):
                print(f'Repo {name} exists!')
            else:
                print(colored("Installed: " + name + " | Use of Plugin is: ",
                              'green',
                              'on_red'))
                for use in plugin['use']:
                    print(colored(use, 'green'))
                clone_repo(repo)


def git_extract_name(git_path):
    splt = git_path.split("/")
    name = splt.pop()
    clean = name.replace(".git", "")
    return clean


def clone_repo(repo_url):
    Repo.clone_from(repo_url,
                    PLUGIN_PATH + git_extract_name(repo_url))


def setup_autocompletion():
    if (is_plugin("deoplete.nvim")):
        print(f'Deoplete exists')
    else:
        print(f'Installing Deoplete')
        clone_repo("https://github.com/Shougo/deoplete.nvim.git")
        clone_repo("https://github.com/roxma/vim-hug-neovim-rpc.git")
        clone_repo("https://github.com/roxma/nvim-yarp.git")
        os.system("apt-get install python3 -y")
        os.system("apt-get install python3-pip")
        os.system("pip3 install neovim")


def is_installed(package):
    return distutils.spawn.find_executable(package)


def install_ctags():
    if not is_installed("ctags"):
        if is_mac():
            os.system("brew install ctags")
        if is_linux():
            os.system("sudo apt-get install ctags highlight -y")


def install_linters():
    pip_linters = ["flake8", "autopep8"]
    for linter in pip_linters:
        if not is_installed(linter):
            os.system("sudo -H pip3 install " + linter)


config = {
    "plugins":
    [{
        "name": "Polygot",
        "description": "Better Syntax Highlighting.",
        "git": ["https://github.com/sheerun/vim-polyglot"],
        "use": ["Disable languages with: let g:polyglot_disabled = ['css']"]
    },
     {
         "name": "Minimalist",
         "description": "A material color scheme for darker vim.",
         "git": ["https://github.com/dikiaap/minimalist"],
         "use": ["In vimrc: colorscheme minimalist"]
     },
     {
         "name": "Monokai Tasty",
         "description": "Sublime Monokai inspired color scheme.",
         "git": ["https://github.com/patstockwell/vim-monokai-tasty.git"],
         "use": ["In vimrc: colorscheme vim-monokai-tasty"]
     },
     {
         "name": "FZF",
         "description": "Fzf File Finder",
         "git": ["https://github.com/junegunn/fzf.git",
                 "https://github.com/junegunn/fzf.vim.git"],
         "use": ["ctrl-p to open",
                 "ctrl-x horizontal split",
                 "ctrl-v vertical split",
                 "ctrl-t new tab"]
     },
     {
         "name": "Lightline",
         "description": "A light and configurable \
         statusline/tabline plugin for Vim",
         "git": ["https://github.com/itchyny/lightline.vim"],
         "use": ['''let g:lightline ={
                       \ 'colorscheme': 'wombat',
                       \ 
                 }''']
     },
     {
         "name": "Tagbar",
         "description": "Displays tags in a window, ordered by scope",
         "git": ["https://github.com/majutsushi/tagbar.git"],
         "use": ["ctrl-t to open",
                 ":T to open, if open jumps to window"]
     },
     {
         "name": "Auto Pairs",
         "description": "Insert or delete brackets, parens, quotes in pair",
         "git": ["https://github.com/jiangmiao/auto-pairs.git"],
         "use": ["Automatic when installed."]
     },
     {
         "name": "Surround",
         "description": "Quoting/parenthesizing made simple.",
         "git": ["https://github.com/tpope/vim-surround.git"],
         "use": ["cs\"' | \"Hello World\" changes to 'Hello World'",
                 "cs'<q> | 'Hello World' changes to <q>Hello World</q>",
                 "ds' 'Hello World' changes to Hello World"]
     },
     {
         "name": "Repeat",
         "description": "Enable repeating supported plugin maps with '.'",
         "git": ["https://github.com/tpope/vim-repeat.git"],
         "use": ["Allows plugins like surround to work with . operator"]
     },
     {
         "name": "Peekaboo",
         "description": "Extends \" and @ in normal mode and <CTRL-R> in \
                    insert mode so you can \
                    see the coontents of the registers.",
         "git": ["https://github.com/junegunn/vim-peekaboo.git"],
         "use": ["press \" or @ for a sidebar to pop up, showing you the \
                 contents of your registers.",
                 "\"add | delete and copy current line into register a.",
                 "\"ap | paste contents of register a to current line"]
     },
     {
         "name": "Easy Motion",
         "description": "Vim motions on speed!",
         "git": ["https://github.com/easymotion/vim-easymotion.git"],
         "use": ["shift-j in normal mode | shows characters for jumping below \
                 cursor.",
                 "shift-k in normal mode | show characters for jumping above \
                 cursor."]
     },
     {
         "name": "Matchit",
         "description": "Extends % matching for HTML, LaTeX, and many \
                        other languages.",
         "git": ["https://github.com/tmhedberg/matchit.git"],
         "use": ["allows % to jump from more robust set of tags"]
     },
     {
         "name": "ZoomWin",
         "description": "Zoom in/out of windows \
                    (toggle between one window and multi-window)",
         "git": ["https://github.com/vim-scripts/ZoomWin.git"],
         "use": ["<CTRL>-O zooms into current VIM pane or zoom out of it.",
                 "CAUTION: Some issues arise when TagBar is open."]
     },
     {
         "name": "Goyo",
         "description": "Distraction-free writing in VIM.",
         "git": ["https://github.com/junegunn/goyo.vim.git"],
         "use": [":G | toggle Goyo on or off.",
                 "let g:goyo_width=100"]
     }],
    "extra_plugins": [{
        "name": "Ale Linter",
        "description": "Asynchronous linting/fixing for Vim and Language Server Protocol (LSP) integration.",
        "git": ["https://github.com/w0rp/ale.git"],
        "use": [":ALEFix | Run through file and attempt to fix mistakes.",
                ":ALEToggle | Turn ALE on or off for the file."]
    }]
}


def main(argv):
    # Add Timezone

    if (not has_word("TZ=", "~/.profile")):
        print(f'Adding timezone.')
        append("~/.profile", "TZ='America/Denver'; export TZ")

    # Setup Config Files
    for src, dst in cp_files.items():
        cp(src, dst)

    setup_autocompletion()
    setup_plugins(config['plugins'])
    setup_plugins(config['extra_plugins'])
    pass


if __name__ == "__main__":
    main(sys.argv)
