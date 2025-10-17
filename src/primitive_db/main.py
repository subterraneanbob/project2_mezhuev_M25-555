#!/usr/bin/env python3

from .engine import welcome


def main():
    print("DB project is running!")

    while welcome() != "exit":
        pass


if __name__ == "__main__":
    main()
