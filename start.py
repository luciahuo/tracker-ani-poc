# The starting command for tool
from Backend.dbutils import client
import colorama
from colorama import Fore, Back, Style

colorama.init()
import argparse
import utils
import pyfiglet
import re
from Backend import dbutils
from dateutil import parser
import datetime

from Objects.Patch import Patch

argparser = argparse.ArgumentParser(description='Process some input files')
argparser.add_argument('--rupstream', type=str)  # path to upstream git repo

args = argparser.parse_args()
fu = args.rupstream

tdb = client.tracker


def load_opening():
    ascii_banner = pyfiglet.figlet_format("Welcome to LSG Patch Tracker")
    print(ascii_banner)
    print(Fore.LIGHTCYAN_EX + 'To get started, run \'help\'')
    print('Here are the statistics:' + Style.RESET_ALL)
    s = dbutils.get_stats()
    print(Fore.LIGHTGREEN_EX + 'Out of ' + str(s['count']) + ' patches in total:' + Style.RESET_ALL)
    print(Fore.LIGHTGREEN_EX + str(s['count_complete']) + Style.RESET_ALL + ' patches are AVAILABLE')
    print(Fore.LIGHTGREEN_EX + str(s['count_incomplete']) + Style.RESET_ALL + ' patches are IN-PROGRESS')
    print(Fore.LIGHTGREEN_EX + '5%' + Style.RESET_ALL + ' RHEL patches are AVAILABLE')
    print(Fore.LIGHTGREEN_EX + '60%' + Style.RESET_ALL + ' UBUNTU patches are AVAILABLE')
    print(Fore.LIGHTGREEN_EX + '27%' + Style.RESET_ALL + ' SLE patches are AVAILABLE')


def parse_populate():  # should be used to one-time load the database
    fup = open(fu)

    commits = utils.changelog_parse(fup.read())
    for c in commits:
        cdt = re.search('(.*) (\+|-)(\d+)', c['commitdate']).group(1)
        dt = parser.parse(cdt)
        p = Patch(
            c['subject'],
            c['hash'],
            c['author'],
            c['email'],
            True,
            dt,
            c['description'],
            datetime.datetime.now()
        )

        tdb.patch.insert_one(p.__dict__)


def run():
    from Backend import dbutils as DB

    # drop the collection
    # DB.clear_database()

    # parse the input files
    # parse_populate()

    # print opening
    load_opening()


if __name__ == '__main__':
    run()
