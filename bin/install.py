import getpass
import re
import sys
from sys import platform
from os.path import expanduser
import os
import argparse


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


def cp(src, dst):
    os.system(add_user("cp -r " + src + " " + dst))


def add_user(file):
    return file.replace("~", expanduser("~"))


def run_sudo(command, password):
    return os.popen("sudo -S %s" % (command), 'w').write(password)


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
            os.system(
                "wget https://github.com/sharkdp/bat/releases/download/v0.10.0/bat-musl_0.10.0_amd64.deb")
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

    if is_installed("npm"):
        os.system("sudo npm -g install instant-markdown-d")
    else:
        print(f'Please install NPM to get Markdown VIM plugin.')


def install_plug():
    os.system("\
    curl -fLo ~/.vim/autoload/plug.vim --create-dirs \
        https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim")


def main(argv):

    # Get sudo pass if flag isn't passed
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

    append_plugin_vimrc()
    install_fzf()
    install_bat(password)
    install_ctags(password)
    install_linters(password)
    install_extra_dirs()
    install_plug()

    if is_mac():
        fix_mac_bash(password)
    pass


if __name__ == "__main__":
    main(sys.argv)
