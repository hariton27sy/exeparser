from core.exe_file import exe_file
import sys


def main():
    if len(sys.argv) < 2 or sys.argv[1] == 'gui':
        print('gui')
        import GUI.gui
        GUI.gui.GUI()
    elif sys.argv[1] == '-c':
        print('console')
        pass  # TODO: make console version
    else:
        print('help')
        pass  # TODO: make help


def test():
    path = 'examples/qoob.exe'
    exe_file(path)


if __name__ == "__main__":
    main()
