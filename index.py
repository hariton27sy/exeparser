#! ./venvubuntu/bin/python3

from core.exefile import ExeFile
import sys


def main():
    try:
        if len(sys.argv) < 2 or sys.argv[1] == '-g':
            print('gui')
            import GUI.gui
            GUI.gui.GUI()
        elif sys.argv[1] == '-c':
            print('console')
            pass  # TODO: make console version
        else:
            print('help')
            pass  # TODO: make help
    except Exception:
        raise  # TODO: make normal output information without strange words


def test():
    path = 'examples/qoob.exe'
    ExeFile(path)


if __name__ == "__main__":
    main()
