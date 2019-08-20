'''
Generates a visual summary of all the patches in the database
'''
import matplotlib.pyplot as plt
from datetime import date
import datetime
import dateutil.relativedelta
from Backend import dbutils


def run():
    stats = dbutils.get_stats()
    f1 = plt.figure(1)
    # generating first graph on states
    states = ['incomplete', 'complete']
    s_states = [stats['count_incomplete'], stats['count_complete']]
    plt.pie(s_states, labels=states, shadow=True)
    plt.legend()
    plt.title("Summary of Patch Completion Since " + str(
        datetime.datetime.now() + dateutil.relativedelta.relativedelta(months=-1)))

    f2 = plt.figure(2)
    d = ['redhat', 'ubuntu', 'suse']
    d_states = [5, 10, 9]
    plt.pie(d_states, labels=d, shadow=True)
    plt.legend()
    plt.title("Patch Summary By Distribution " + str(date.today()))

    plt.show()


if __name__ == '__main__':
    run()
