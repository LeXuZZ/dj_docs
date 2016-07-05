from subprocess import STDOUT, check_call
import os


def put_config_files():
    pass


def install_requirements():
    pass


def upgrade_system():
    check_call(['apt-get', 'update'], stdout=open(os.devnull, 'ws'), stderr=STDOUT)


def main():
    upgrade_system()

if __name__ == '__main__':
    main()