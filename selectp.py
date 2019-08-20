import argparse
from dateutil import parser as dparser
import json
from prettytable import PrettyTable
import colorama
from colorama import Fore, Back, Style
import re
import sys

colorama.init()
import utils

parser = argparse.ArgumentParser()
parser.add_argument('--subject', '-s', help='regex to match to subject')
parser.add_argument('--hash', nargs='+',
                    help='search by upstream hash of the patch or multiple patches separated by spaces')
parser.add_argument('--firstname', '-fn', help='first name of patch author')
parser.add_argument('--lastname', '-ln', help='last name of patch author')
parser.add_argument('-upstream', action='store_true', help='flag indicating whether a patch is already upstream')
parser.add_argument('--after', help='shows commits more recent than a specific date, formatted YYYY-MM-DD')
parser.add_argument('--before', help='shows commits before a specific date, formatted YYYY-MM-DD')
parser.add_argument('--grepdescription', '-grep', help='show only commands with descriptions that match a specific ')
parser.add_argument('--priority', choices={'1', '2', '3'},
                    help='higher than priority, options are highest 1, 2 or lowest 3')
parser.add_argument('--dkernel', choices={'ubuntu', 'rhel', 'sle'}, type=str.lower, help='distribution kernel')
parser.add_argument('-all', '-a', action='store_true', help='show all patches')
parser.add_argument('-verbose', '-v', action='store_true', help='show details for all patch outputs')
parser.add_argument('--output', '-o', choices={'table', 'json'}, default='json',
                    help='output in either json or table view')
parser.add_argument('--sort', choices={'commitdate', 'priority', 'lastmodified'}, default='lastmodified',
                    help='sort the output')

args = parser.parse_args()
'''
Takes the condition of the arguments and turns them into a query for mongo
'''


def query_builder(args):
    q = {}

    if args.hash:
        q['uhash'] = {'$in': args.hash}

    if args.subject:
        q['subject'] = {'$regex': args.subject, '$options': 'i'}

    if args.firstname and args.lastname is None:
        q['author'] = {'$regex': args.firstname + ' (.*)', '$options': 'i'}
    if args.lastname and args.firstname is None:
        q['author'] = {'$regex': '(.*) ' + args.lastname, '$options': 'i'}
    if args.lastname and args.firstname:
        q['author'] = {'$regex': args.firstname + ' ' + args.lastname, '$options': 'i'}

    if args.upstream:
        q['upstream'] = True

    if args.after and args.before is None:
        q['commitdate'] = {'$gte': dparser.parse(args.after)}
    if args.before and args.after is None:
        q['commitdate'] = {'$lt': dparser.parse(args.before)}
    if args.before and args.after:
        q['commitdate'] = {'$gte': dparser.parse(args.after), '$lt': dparser.parse(args.before)}

    if args.grepdescription:
        q['description'] = {'$regex': args.grepdescription, '$options': 'i'}

    if args.priority:
        q['priority'] = {'$gte': int(args.priority)}

    if not args.all or args.dkernel:
        if args.all and args.dkernel:
            q['distro'] = {'$elemMatch': {'name': args.dkernel}}
        elif args.dkernel:
            q['distro'] = {'$elemMatch': {'name': args.dkernel, 'state': {'$regex' : '^((?!AVAILABLE).)*$', '$options' : 'i'}}}
        elif not args.all:  # show only patches that are not complete
            q['distro'] = {'$elemMatch': {'state': {'$regex' : '^((?!AVAILABLE).)*$', '$options' : 'i'}}}

    return q


def print_output(results):
    if args.output is 'json':
        if args.verbose:
            for p in results:
                print(utils.prettify_json(json.dumps(p, sort_keys=True, indent=4, default=str)))
        else:
            for p in results:
                o = utils.simplify_patch_output(p)
                print(utils.prettify_json(json.dumps(o, sort_keys=True, indent=4, default=str)))
    else:
        x = PrettyTable()

        x.field_names = ['Patch', 'Priority', 'ubuntu/18.04', 'rhel/8', 'sle/12-SP4-AZURE']

        for p in results:
            x.add_row([Fore.LIGHTCYAN_EX + p['uhash'] + Style.RESET_ALL +
                       '\n' + Fore.LIGHTMAGENTA_EX + p['subject'] + Style.RESET_ALL,
                       p['priority'],
                       next(d for d in p['distro'] if d['name'] == 'ubuntu' and d['release'] == '18.04')['state'],
                       next(d for d in p['distro'] if d['name'] == 'rhel' and d['release'] == '8')['state'],
                       next(d for d in p['distro'] if d['name'] == 'sle' and d['release'] == '12-SP4-AZURE')['state']])

        print(x)


def sort(r):
    if args.sort is 'lastmodified':
        r.sort("datemodified", -1)
    elif args.sort is 'commitdate':
        r.sort("commitdate", -1)
    else:
        r.sort("priority", 1)

    return r


def run():
    from Backend import dbutils as DB

    q = query_builder(args)

    results = DB.select_patch(q)
    s_results = sort(results)
    s_results.count()

    sys.stdout.write(Fore.LIGHTCYAN_EX + 'returning ' + str(s_results.count()) + ' patches' + Style.RESET_ALL)

    print_output(s_results)
    # for p in s_results:
    #     DB.delete_patch(p)


if __name__ == '__main__':
    run()
