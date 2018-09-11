Ethan Wright dotfiles with setup </br>

All dotfiles are stored in the conf/ directory of this repo. Current list
includes 
* bashrc
* vim 
* tmux

## To install:
```
cd ~/dotfiles/bin
./install.sh
```

### If you want the linter plugin setup:
```
cd ~/dotfiles/bin
./install.sh -l
```

If an existing version of the file exists it will be overwritten

Utility also exists to remove all currently existing versions of the dot files
with 
```
bin/cleanup.sh
```


