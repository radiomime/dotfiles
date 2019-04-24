import json
import distutils
import re
import sys
from sys import platform
from os.path import expanduser
import os
import argparse

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
    "../conf/skeletons": "~/.vim",
    "../conf/vimrc": "~/.vimrc",
    "../conf/linters/*": "~",
    "../conf/fzf_functions": "~/.fzf_functions"
}


def cp(src, dst):
    os.system(add_user("cp -r " + src + " " + dst))


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


def setup_plugins(plugin_list):
    append_plugin_vimrc()

    for plugin in plugin_list:
        for repo in plugin['git']:
            name = git_extract_name(repo)

            if(is_plugin(name)):
                print(f'==============================================')
                print(f'Repo {name} exists!                          |')
                print(f'==============================================')
            else:
                print(f'==============================================')
                print(f'Installed: {name} | Use of Plugin is: ')
                print(f'----------------------------------------------')
                for use in plugin['use']:
                    print(f'             | {use}')
                print(f'----------------------------------------------')
                clone_repo(repo)


def git_extract_name(git_path):
    splt = git_path.split("/")
    name = splt.pop()
    clean = name.replace(".git", "")

    return clean


def clone_repo(repo_url):
    os.system(f'git clone {repo_url} {PLUGIN_PATH + git_extract_name(repo_url)}')


def setup_autocompletion():
    if (is_plugin("deoplete.nvim")):
        print(f'Deoplete exists')
    else:
        print(f'Installing Deoplete')
        clone_repo("https://github.com/Shougo/deoplete.nvim.git")
        clone_repo("https://github.com/roxma/vim-hug-neovim-rpc.git")
        clone_repo("https://github.com/roxma/nvim-yarp.git")

        if (is_linux()):
            os.system("sudo apt-get install python3 -y")
            os.system("sudo apt-get install python3-pip")
        os.system("python3 -m pip install neovim")


def is_directory(path):
    return os.path.isdir(add_user(path))


def is_installed(package):
    return distutils.spawn.find_executable(package)


def install_ctags():
    if not is_installed("ctags"):
        if is_mac():
            os.system("brew install ctags -y")

        if is_linux():
            os.system("sudo apt-get install ctags highlight -y")


def install_fzf():
    if not is_directory("~/.fzf"):
        if is_mac():
            print(f'Installing FZF using brew...')
            os.system("brew install fzf -y")
        else:
            print(f'Installing FZF from git...')
            os.system(
                add_user("git clone --depth 1 https://github.com/junegunn/fzf.git ~/.fzf"))
            os.system("~/.fzf/install --all")
    else:
        print(f'FZF already installed. {is_directory("~/.fzf")}')


def install_linters():
    pip_linters = ["flake8", "autopep8"]

    for linter in pip_linters:
        if not is_installed(linter):
            os.system("sudo -H pip3 install " + linter)


def filter_impact(plugins, impact):
    if impact == "heavy":
        return plugins
    filtered = []
    if impact == "medium":
        for plugin in plugins:
            if plugin["impact"] == "medium" or plugin["impact"] == "light":
                filtered.push(plugin)
    if impact == "light":
        for plugin in plugins:
            if plugin["impact"] == "light":
                filtered.append(plugin)
    return filtered


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--impact", type=str, help="levels are: light, medium, heavy. Plugin weight")
    args = parser.parse_args()

    # Add Timezone

    if (not has_word("TZ=", "~/.profile")):
        print(f'Adding timezone.')
        append("~/.profile", "TZ='America/Denver'; export TZ")

    # Setup Config Files
    os.system("mkdir -p ~/.vim/autoload")
    os.system("mkdir -p ~/.vim/colors")

    for src, dst in cp_files.items():
        cp(src, dst)

    # TODO: Add flags for different levels of install

    setup_autocompletion()
    if args.impact:
        plugin_list = filter_impact(config['plugins'], args.impact)
    else:
        plugin_list = config['plugins']

    setup_plugins(plugin_list)
    setup_plugins(config['extra_plugins'])
    install_fzf()
    pass


if __name__ == "__main__":
    main(sys.argv)
