import re
from pygments import highlight, lexers, formatters


# takes in a changelog file as a string
def changelog_parse(changelogf):
    changeloglines = changelogf.splitlines()
    commits = []
    # dict to store commit data
    commit = {}
    # iterate lines and save
    for nextLine in changeloglines:
        if nextLine == '' or nextLine == '\n':
            # ignore empty lines
            pass
        elif bool(re.match('commit', nextLine, re.IGNORECASE)):
            # commit xxxx
            if len(commit) != 0:  # new commit, so re-initialize
                commits.append(commit)
                commit = {}
            commit = {'hash': re.match('commit (.*)', nextLine, re.IGNORECASE).group(1)}
        elif bool(re.match('merge:', nextLine, re.IGNORECASE)):
            # Merge: xxxx xxxx
            pass
        elif bool(re.match('author:', nextLine, re.IGNORECASE)):
            # Author: xxxx <xxxx@xxxx.com>
            m = re.compile('Author: (.*) <(.*)>').match(nextLine)
            commit['author'] = m.group(1)
            commit['email'] = m.group(2)
        elif bool(re.match('date:', nextLine, re.IGNORECASE)):
            # Date: xxx
            dt = re.compile('Date: (.*)').match(nextLine)
            commit['commitdate'] = dt.group(1).strip()
        elif bool(re.match('    ', nextLine, re.IGNORECASE)):
            # (4 empty spaces)
            if commit.get('subject') is None:
                commit['subject'] = nextLine.strip()
            else:
                if commit.get('description') is None:
                    commit['description'] = nextLine.strip()
                else:
                    commit['description'] = commit['description'] + "\n" + nextLine
        else:
            print('ERROR: Unexpected Line: ' + nextLine)
    return commits


'''
Takes full patch info and returns simplified object
'''


def simplify_patch_output(p):
    o = {
        'subject': p['subject'],
        'priority': p['priority'],
        'hash': p['uhash'],
        'commit date': p['commitdate'],
        'distro': p['distro'],
    }
    return o


def prettify_json(json):
    return highlight(json, lexers.JsonLexer(), formatters.TerminalFormatter())
