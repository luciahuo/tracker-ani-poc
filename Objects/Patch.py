from .DKernel import DKernel
import random


class Patch:
    def __init__(self, subject, uhash, author, email, upstream, commitdate, description, datemodified):
        self.subject = subject  # identifier for the patch,
        self.uhash = uhash  # upstream hash
        self.author = author
        self.email = email
        self.upstream = upstream
        # dummy link
        self.upstreamlink = 'https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=12345'
        self.commitdate = commitdate
        self.description = description
        self.priority = 2  # default - there are only priorities 1, 2 and 3
        self.distro = self.connect_to_distros()
        self.related_commits = []
        self.parent_commits = []
        self.datemodified = datemodified  # date last modified
        self.modhistory = []  # modification history

    '''
    Returns a list of distributions
    '''

    def connect_to_distros(self):
        dlist = []
        states = ['ACCEPTED - linux-next',
                  'PENDING - distro',
                  'ACCEPTED - distro',
                  'TESTING - microsoft',
                  'SIGNED-OFF - microsoft',
                  'AVAILABLE TO CUSTOMER',
                  'AVAILABLE IN AZURE']  # states enum
        # creates a list of distribution objects
        for d in ['ubuntu/18.04', 'rhel/8', 'sle/12-SP4-AZURE']:
            dlist.append(DKernel(
                d.split('/')[0],  # distro
                d.split('/')[1],  # release
                random.choice(states),  # fake state
                random.randint(1, 1001),  # fake bug id
                'https://bugzilla.distro.com/show_bug.cgi?id=12345'  # dummy link
            ).__dict__)
        return dlist
