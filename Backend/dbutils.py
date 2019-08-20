import pymongo
import datetime

# global database client
client = pymongo.MongoClient('localhost', 27017)
tdb = client.tracker  # creating the database called tracker


def get_all_patch():
    return tdb.patch.find({})


'''
Given a query get patches that match conditions specified
'''


def select_patch(query):
    return tdb.patch.find(query)


'''
Given an updated patch update patch in database
'''


def edit_patch(obj, changes):
    # modify the date modified field
    obj['datemodified'] = datetime.datetime.now()
    changess = "fields:"
    for c in changes:
        changess += " " + c
    # add to modified history field
    if changes:
        obj['modhistory'].append(changess + " were modified on " + str(datetime.datetime.now()))

    tdb.patch.replace_one(
        {'uhash': obj['uhash']},
        obj
    )


'''
Delete patch
'''


def delete_patch(obj):
    tdb.patch.remove(obj)
    print('a patch has been removed')


'''
Given a patch json string, add it to the database
'''


def add_patch(obj):
    tdb.patch.insert_one(obj)
    print('new upstream patch was inserted successfully!')


'''
Get statistics for all the patches
'''


def get_stats():
    s = {}
    s['count'] = tdb.patch.find({}).count()
    s['count_complete'] = tdb.patch.find(
        {'distro': {'$not': {'$elemMatch': {'state': {'$regex': 'AVAILABLE'}}}}}).count()
    s['count_incomplete'] = s['count'] - s['count_complete']
    s['p_rh_complete'] = tdb.patch.find(
        {'distro': {'$elemMatch': {'state': {'$regex': 'AVAILABLE'}, 'name': 'rhel'}}}).count()
    s['p_ubuntu_complete'] = tdb.patch.find(
        {'distro': {'$elemMatch': {'state': {'$regex': 'AVAILABLE'}, 'name': 'ubuntu'}}}).count()
    s['p_suse_complete'] = tdb.patch.find(
        {'distro': {'$elemMatch': {'state': {'$regex': 'AVAILABLE'}, 'name': 'sle'}}}).count()

    return s


def clear_database():
    tdb.patch.drop()
    print('collection dropped')
