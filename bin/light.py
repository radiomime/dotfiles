from os.path import expanduser
import sys
import argparse
import json
import os

with open('./plugins.json') as json_file:
    config = json.load(json_file)

cp_files = {
    "../conf/bashrc": "~/.bashrc",
    "../conf/bin": "~/.bin",
    "../conf/functions": "~/.functions",
    "../conf/public_aliases": "~/.public_aliases",
    "../conf/tmux.conf": "~/.tmux.conf",
    "../conf/vim_colors/*.vim": "~/.vim/colors",
    "../conf/autoload/*": "~/.vim/autoload/",
    "../conf/skeletons/": "~/.vim/",
    "../conf/vimrc": "~/.vimrc",
    "../conf/linters/*": "~",
    "../conf/fzf_functions": "~/.fzf_functions"
}


def add_user(file):
    return file.replace("~", expanduser("~"))


PLUGIN_PATH = add_user("~/.vim/bundle/")


def cp(src, dst):
    os.system(add_user("cp -r " + src + " " + dst))


def append(file, text):
    open(add_user(file), "a+")\
        .write(text)


def is_plugin(file):
    if os.path.isdir(PLUGIN_PATH + file):
        return True
    return False


def append_plugin_vimrc():
    os.system("cp ../conf/vimrc " + add_user("~/.vimrc"))

    fin = open("../conf/vimrc_plugin", "r")
    data2 = fin.read()
    fin.close()
    fout = open(add_user("~/.vimrc"), "a")
    fout.write(data2)
    fout.close()


def git_extract_name(git_path):
    splt = git_path.split("/")
    name = splt.pop()
    clean = name.replace(".git", "")
    return clean


def clone_repo(repo_url):
    line = "git clone " + repo_url + " " + PLUGIN_PATH  + git_extract_name(repo_url)
    os.system(line)


def setup_plugins(plugin_list):
    append_plugin_vimrc()

    for plugin in plugin_list:
        for repo in plugin['git']:
            name = git_extract_name(repo)

            if(is_plugin(name)):
                print("==============================================")
                print("Repo " + name + " exists!                          |")
                print("==============================================")
            else:
                print("==============================================")
                print("Installed: " + name + " | Use of Plugin is:   ")
                print("----------------------------------------------")

                for use in plugin['use']:
                    print("             | " + use)
                print("----------------------------------------------")
                clone_repo(repo)


def main(argv):
    # Setup Config Files
    os.system("mkdir -pv ~/.vim/autoload")
    os.system("mkdir -pv ~/.vim/colors")

    # Setup sessions directory
    os.system("mkdir -pv ~/.vim/sessions")

    # Setup dotfiles
    for src, dst in cp_files.items():
        cp(src, dst)

    # Setup plugins
    setup_plugins(config['plugins'])
    pass


if __name__ == "__main__":
    main(sys.argv)
