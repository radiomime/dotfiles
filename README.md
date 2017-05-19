Ethan Wright dotfiles with setup </br>

All dotfiles are stored in the conf/ directory of this repo. Current list
includes 
* bashrc
* vim 
* tmux

The code in the bin/ directory used to setup the dot files easily in a given environment 
* linux_setup
* mac_setup
* other_setup_all.sh

The mac and linux setup allows for flags to specify the files to install, e.g.
```
bin/mac_setup -a 
bin/mac_setup -v
bin/mac_setup -t 
bin/mac_setup -b 
```
These flags will set up: 
* all dotfiles
* vim dotfiles and config
* tmux config file
* bashrc file

If an existing version of the file exists it will be overwritten

Utility also exists to remove all currently existing versions of the dot files
with 
```
bin/cleanup.sh
```


