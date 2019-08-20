import argparse
import sys, tempfile, os
from subprocess import call
from Backend import dbutils
from bson import json_util
import utils
import colorama
import json
from colorama import Fore, Back, Style
colorama.init()

parser = argparse.ArgumentParser()
parser.add_argument('hash', help='hash identifier of a patch')

args = parser.parse_args()

def run():
    EDITOR = os.environ.get('EDITOR', 'vim')

    # get the patch
    try:
        p = dbutils.select_patch({'uhash': args.hash}).next()
    except StopIteration:
        print("Empty cursor!")

    pjson = json_util.dumps(p, indent=4, sort_keys=True)
    s = pjson.encode('UTF-8')

    with tempfile.NamedTemporaryFile(suffix=".tmp") as tf:
        tf.write(s)
        tf.flush()
        call([EDITOR, tf.name])

        tf.seek(0)
        edited_message = tf.read()

        # load the object from string

        newobj = json_util.loads(edited_message.decode("utf-8"))
        changes = [] # list of things that changed
        if newobj['subject'] != p['subject']:
            changes.append("subject")
        if newobj['author'] != p['author']:
            changes.append("author")
        if newobj['description'] != p['description']:
            changes.append("description")
        if newobj['priority'] != p['priority']:
            changes.append("priority")

        # send updated object to the database
        dbutils.edit_patch(newobj, changes)

        print(Fore.LIGHTCYAN_EX)
        print('Patch ' + args.hash + ' has been modified')
        print(Style.RESET_ALL)
        try:
            p = dbutils.select_patch({'uhash': args.hash}).next()
        except StopIteration:
            print("Empty cursor!")
        print(utils.prettify_json(json.dumps(p, sort_keys=True, indent=4, default=str)))

if __name__ == '__main__':
    run()