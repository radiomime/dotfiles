# ToDo

## Fresh Install for System:
* establish mac vs ubuntu
* Install yarn
* Install docker
* Install npm
* npm install `n`
* npm update global packages?

## General
* Using `source` to reference other files?
    * https://www.reddit.com/r/vim/comments/1zqohb/do_you_use_one_big_vimrc_file_for_all_your/
    * https://www.gregjs.com/vim/2016/do-yourself-a-favor-and-modularize-your-vimrc-init-vim/
* Vim in multiple files
    * for different file types, using after and `ftplugins`
    * https://unix.stackexchange.com/questions/171132/can-vimrc-be-divided-into-multiple-files
* other things
* vimrc to ~/.vim/ ?

## References
* checkout : https://learnvimscriptthehardway.stevelosh.com/

# Overview
dotfiles with setup. </br>

All dotfiles are stored in the conf/ directory of this repo. Current list
includes
* bashrc
* vim
* tmux

## Setup:
Requires Python 3.6 and vim 8.

On Ubuntu:
```
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo add-apt-repository ppa:jonathonf/vim -y 
sudo apt-get update
sudo apt-get install -y python3.6 vim
```

## To install:
```
cd ~/dotfiles/bin
python3.6 install.py -i <weight>
```

If an existing version of the file exists it will be overwritten

Utility also exists to remove all currently existing versions of the dot files
with
```
bin/cleanup.sh
```

Original commit courtesy of [Ethan Wright](https://github.com/EthanJWright).
