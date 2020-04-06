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
