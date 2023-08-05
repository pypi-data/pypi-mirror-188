import sys

from cloud9_cli.command import Command


def main():
    try:
        Command()

    except KeyboardInterrupt:
        print('Cancelled by user.')
        sys.exit()


if __name__ == '__main__':
    main()
