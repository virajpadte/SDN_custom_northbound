#!/usr/bin/python

import MySQLdb
import json


def get_grps():
    # Open database connection
    db = MySQLdb.connect(host, user, passwd, db_name)
    # testing connection:
    if db.open:
        print("connection is established")
    else:
        print("could not establish connection. Check credentials or connects sysops admin")
    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    # Prepare SQL query to get data from the table
    query = "SELECT DISTINCT group_id FROM hosts"
    try:
        # Execute the SQL command
        cursor.execute(query)
        # Fetch all the rows in a list of lists.
        results = cursor.fetchall()
        # print received data:
        print(results)
        return results
    except MySQLdb.Error, e:
        print("exception occured")
        print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
        # Rollback in case there is any error
        db.rollback()
    # disconnect from server
    db.close()


def get_host_list(grp_id):
    # Open database connection
    db = MySQLdb.connect(host, user, passwd, db_name)
    # testing connection:
    if db.open:
        print("connection is established")
    else:
        print("could not establish connection. Check credentials or connects sysops admin")
    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    # Prepare SQL query to get data from the table
    query = "SELECT host_id FROM hosts WHERE group_id=%s"
    try:
        # Execute the SQL command
        cursor.execute(query, (grp_id))
        # Fetch all the rows in a list of lists.
        host_list = cursor.fetchall()
        # print received data:
        for host_entry in host_list:
            print(host_entry[0])
        return host_list

    except MySQLdb.Error, e:
        print("exception occured")
        print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
        # Rollback in case there is any error
        db.rollback()
    # disconnect from server
    db.close()


def make_payload(ip_list, grp_list, policy_list):
    payload = {}
    master_grp = {}
    grp_dict_list = []
    for idx, grp in enumerate(grp_list):
        grp = {}
        grp["host_ips"] = ip_list[idx]
        master_grp[grp_list[idx]] = grp
    payload["Groups"] = [master_grp]
    # add policies
    payload["Policy"] = [policy_list]
    return payload


def update_controller():
    grp_list = get_grps()
    for grp in grp_list:
        # getting a host list for each unique grp
        host_list = get_host_list(grp[0])


if __name__ == "__main__":
    # get json credentials
    with open('config.json') as json_data_file:
        data = json.load(json_data_file)
    host = data["mysql"]["host"]
    user = data["mysql"]["user"]
    passwd = data["mysql"]["passwd"]
    db_name = data["mysql"]["db"]
    grp_list = get_grps()
    for grp in grp_list:
         # getting a host list for each unique grp
         #get_host_list(grp[0])
        print(grp)
