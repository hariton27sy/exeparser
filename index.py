#! /usr/bin/python3

import sys

import CLI.cli


def main():
    try:
        CLI.cli.CommandLineInterface(sys.argv[1:])
    except KeyboardInterrupt:
        print("Stopped by user")
    except Exception as e:
        print(f"{e}\nExit with code 1...")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
