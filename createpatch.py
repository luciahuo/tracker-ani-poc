"""
takes a patch from patch.json and puts it in database for demo purposes
"""
import argparse
from Backend import dbutils
import json

parser = argparse.ArgumentParser()
# takes in the entire patch string
parser.add_argument('--upstream')

args = parser.parse_args()


def run():
    with open(args.upstream) as f:
        o = json.load(f)  # get the object
        dbutils.add_patch(o)


if __name__ == '__main__':
    run()
