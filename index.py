#! /usr/bin/python3

from core.exefile import ExeFile
import sys
import subprocess


def main():
    try:
        if len(sys.argv) > 1 and sys.argv[1] == '-g':
            import GUI.gui
            GUI.gui.GUI(sys.argv[2:])
        else:
            import CLI.cli
            CLI.cli.CommandLineInterface(sys.argv[1:])
    except Exception as e:
        raise  # TODO: make normal output information without strange words


def test():
    path = 'examples/qoob.exe'
    ExeFile(path)


if __name__ == "__main__":
    main()
