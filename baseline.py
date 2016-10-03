import os
import sys


# python baseline.py "train/"


def main():
    for fn in os.listdir("train/"):
        with open("train/" + fn) as f:
            lines = f.readlines()
            print(lines)



if __name__ == '__main__':
  main()
