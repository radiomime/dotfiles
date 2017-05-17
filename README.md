Ethan Wright Dot Files with Setup </br>

All dot files are stored in the conf/ directory of this repo. Current list
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
bin/mac_setup -v -t
```

Utility also exists to remove all currently existing versions of the dot files
with 
```
bin/cleanup.sh
```


