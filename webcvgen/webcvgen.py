#!/usr/bin/env python3
from webgen import generate_website
import sys
from os.path import exists

def print_help():
    print()
    print("Online CV Generation Script")
    print("=============================================================")
    print("Usage:")
    print("webcvgen cv.yaml out.html")
    print()
    print(" - cv.yaml: A yaml file representing a cv")
    print(" - out.html: Optional output filename, defaults to index.html")
    print("=============================================================")
    print("When run with no arguments, print this help message")
    print()


# Parse inputs for filenames
if len(sys.argv) == 1:
    print_help()
    exit()
elif len(sys.argv) == 2:
    cvfile = sys.argv[1]
    savefile = "index.html"
else:
    cvfile = sys.argv[1]
    savefile = sys.argv[2]

if exists(savefile):
    while True:
        answer = input(f"{savefile} exists. Overwrite? (y/n)\n")
        if answer.upper() in ["Y", "YES"]:
            break
        elif answer.upper() in ["N", "NO"]:
            print("Cancelling Webpage Generation...")
            exit()

generate_website(savefile, cvfile)
