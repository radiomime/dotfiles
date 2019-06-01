import getpass
import json
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

def run_sudo(command, password):
    return os.popen("sudo -S %s"%(command), 'w').write(password)

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


def fix_mac_bash(password):
    # Update Mac Bash shell

    if is_mac():
        os.system("brew install bash")
        os.system("chsh -s /usr/local/bin/bash")
        command = "bash -c 'echo /usr/local/bin/bash >> /etc/shells'"
        if password is not None:
            run_sudo(command, password)
        else:
            os.system(command)
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


def setup_autocompletion(password):
    if (is_plugin("deoplete.nvim")):
        print(f'Deoplete exists')
    else:
        print(f'Installing Deoplete')
        clone_repo("https://github.com/Shougo/deoplete.nvim.git")
        clone_repo("https://github.com/roxma/vim-hug-neovim-rpc.git")
        clone_repo("https://github.com/roxma/nvim-yarp.git")

        if (is_linux()):
            command = "apt-get install -y python3 python3-pip"
            if password is not None:
                run_sudo(command, password)
            else:
                os.system(command)
        os.system("python3 -m pip install neovim")


def is_directory(path):
    return os.path.isdir(add_user(path))


def is_installed(package):
    return os.popen('which ' + package).read() != ""


def install_ctags(password):
    if not is_installed("ctags"):
        if is_mac():
            os.system("brew install ctags")

        if is_linux():
            command = "apt-get install ctags highlight -y"
            if password is not None:
                run_sudo(command, password)
            else:
                os.system(command)

def install_fzf():
    if not is_directory("~/.fzf"):
        if is_mac():
            print(f'Installing FZF using brew...')
            os.system("$(brew --prefix)/opt/fzf/install --all")
        else:
            print(f'Installing FZF from git...')
            os.system(
                add_user("git clone --depth 1 https://github.com/junegunn/fzf.git ~/.fzf"))
            os.system("~/.fzf/install --all")
    else:
        print(f'FZF already installed. {is_directory("~/.fzf")}')


def install_bat(password):
    if not is_installed('bat'):
        print(f'Installing BAT | usage : bat file')

        if (is_linux()):
            os.system("wget https://github.com/sharkdp/bat/releases/download/v0.10.0/bat-musl_0.10.0_amd64.deb")
            command = "dpkg -i bat-musl_0.10.0_amd64.deb"
            if password is not None:
                run_sudo(command, password)
            else:
                os.system(command)
            os.system("rm bat-musl_0.10.0_amd64.deb")

        if (is_mac()):
            os.system("brew install bat")
    else:
        print(f'BAT already installed!')


def install_linters(password):
    pip_linters = ["flake8", "autopep8"]
    npm_linters = ["eslint"]

    for linter in npm_linters:
        if not is_installed(linter) and is_installed("npm"):
            os.system("npm install -g " + linter)

    for linter in pip_linters:
        if not is_installed(linter):
            command = "python3 -m pip install " + linter
            if password is not None:
                run_sudo(command, password)
            else:
                os.system(command)


def install_extra_dirs():
    os.system("mkdir -pv ~/.sandbox")
    os.system("mkdir -pv ~/.notes")
    if not is_plugin('markdown'):
        if is_installed("npm"):
            os.system("sudo npm -g install instant-markdown-d")
            os.system("git clone https://github.com/suan/vim-instant-markdown.git ~/.vim/bundle/markdown")
        else:
            print(f'Please install NPM to get Markdown VIM plugin.')


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
    parser.add_argument("-i", "--impact", type=str, help="levels are: light, medium, heavy : -i heavy")
    parser.add_argument('--noroot', help='if noroot is set, will not ask for sudo pass or run things with sudo.')
    args = parser.parse_args()

    # Get sudo pass if flag isn't passed
    password = None
    if not args.noroot:
        password = getpass.getpass("Enter your admin password:")

    # Add Timezone

    if (not has_word("TZ=", "~/.profile")):
        print(f'Adding timezone.')
        append("~/.profile", "TZ='America/Denver'; export TZ")

    # Setup Config Files
    os.system("mkdir -pv ~/.vim/autoload")
    os.system("mkdir -pv ~/.vim/colors")

    # Setup sessions directory
    os.system("mkdir -pv ~/.vim/sessions")

    for src, dst in cp_files.items():
        cp(src, dst)

    # TODO: Add flags for different levels of install

    setup_autocompletion(password)

    if args.impact:
        plugin_list = filter_impact(config['plugins'], args.impact)
    else:
        plugin_list = config['plugins']

    setup_plugins(plugin_list)

    if not args.impact or args.impact == "heavy":
        setup_plugins(config['extra_plugins'])
        install_fzf()
        install_bat(password)
        install_ctags(password)
        install_linters(password)
        install_extra_dirs()
    pass


if __name__ == "__main__":
    main(sys.argv)
