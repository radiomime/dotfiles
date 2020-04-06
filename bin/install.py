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


def br(w):
    print("|" + '-' * w + "|")


def banner(w, word):
    br(w)
    mid = int((w - len(word)) / 2)
    print("|" + (mid * " ") + word + (mid * " ") + "|")
    br(w)


def gen_install(name, why, cmd):
    return {'name': name, 'why': why, 'cmds': cmd}


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


def is_file(path):
    return os.path.exists(add_user(path))


def is_installed(package):
    return os.popen('which ' + package).read() != ""


def is_npm_installed(package):
    return os.popen('npm list -g ' + package +
                    "|grep " + package).read() != ""


def install_ctags():
    if not is_installed("ctags"):
        name = "ctags"
        why = "Allows tag generation for code bases, \
            enables jumping to definitions."
        cmds = []
        if is_mac():
            cmds.append("brew install ctags")
        if is_linux():
            cmds.append("apt-get install ctags highlight -y")
        return gen_install(name, why, cmds)
    else:
        return None


def install_fzf():
    if not is_directory("~/.fzf"):
        name = "FZF"
        why = "Fuzzy finding for command line, ctrl-r better and more"
        cmds = []
        if is_mac():
            cmds.append("$(brew --prefix)/opt/fzf/install --all")
        else:
            cmds.append(
                add_user("git clone --depth 1 https://github.com/junegunn/fzf.git ~/.fzf"))
            cmds.append("~/.fzf/install --all")
            return gen_install(name, why, cmds)
    else:
        return None


def install_bat():
    if not is_installed('bat'):
        name = "BAT"
        why = "utility like cat, but prettier"
        commands = []

        if (is_linux()):
            commands.append("wget \
                            https://github.com/sharkdp/bat\
                            /releases/download/v0.10.0/bat-\
                            musl_0.10.0_amd64.deb")
            commands.append("dpkg -i bat-musl_0.10.0_amd64.deb")
            commands.append("rm bat-musl_0.10.0_amd64.deb")
        if (is_mac()):
            commands.append("brew install bat")
        return gen_install(name, why, commands)
    else:
        return None


def install_linters():
    pip_linters = ["flake8", "autopep8"]
    npm_linters = ["eslint"]

    name = "Linters for python and nodejs"
    why = "Enables syntax suggestions & standard adhesion"
    cmds = []
    for linter in npm_linters:
        if not is_installed(linter) and is_installed("npm"):
            cmds.append("npm install -g " + linter)
    for linter in pip_linters:
        if not is_installed(linter):
            cmds.append("python3 -m pip install " + linter)
    if len(cmds) != 0:
        return gen_install(name, why, cmds)
    else:
        return None


def install_npm_md():
    if not is_installed("npm"):
        return None

    if is_npm_installed("instant-markdown-d"):
        return None

    name = "instant-markdown"
    why = "Enables live render of markdown through plugin"
    cmds = []
    cmds.append('sudo npm install -g instant-markdown-d')
    return gen_install(name, why, cmds)


def install_extra_dirs():
    os.system("mkdir -pv ~/.sandbox")
    os.system("mkdir -pv ~/.notes")


def install_plug():
    if (is_file("~/.vim/autoload/plug.vim")):
        return None

    name = "Plug"
    why = "Plugin Manager for VIM. \
        Open vim and run :PlugInstall to install plugins."
    cmds = []

    cmds.append("\
    curl -fLo ~/.vim/autoload/plug.vim --create-dirs \
        https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim")
    return gen_install(name, why, cmds)


def main(argv):
    w = 70  # width of banners
    inform = []
    # Add Timezone
    if (not has_word("TZ=", "~/.profile")):
        print('Adding timezone.')
        append("~/.profile", "TZ='America/Denver'; export TZ")

    # Setup Config Files
    os.system("mkdir -pv ~/.vim/autoload")
    os.system("mkdir -pv ~/.vim/colors")

    # Setup sessions directory
    os.system("mkdir -pv ~/.vim/sessions")

    for src, dst in cp_files.items():
        cp(src, dst)

    append_plugin_vimrc()
    inform.append(install_fzf())
    inform.append(install_bat())
    inform.append(install_ctags())
    inform.append(install_linters())
    inform.append(install_plug())
    inform.append(install_npm_md())
    install_extra_dirs()

    def remove_none(item):
        return item is not None

    inform = list(filter(remove_none, inform))
    if (len(inform) == 0):
        return

    def out(text):
        print(text)

    def instruct(install):
        br(w)
        print('To install: ' + install['name'])
        print('For: ' + install['why'])
        print('Run: ')
        br(w)
        [out(cmd) for cmd in install['cmds']]

    banner(w, "Extra Libraries")
    print("It looks like you are missing some libraries utilized by \
        the best vim plugins, to install these, you can run: ")
    [instruct(item) for item in inform]

    banner(w, 'Or install everything:')
    for item in inform:
        [out(cmd) for cmd in item['cmds']]
    br(w)


if __name__ == "__main__":
    main(sys.argv)
