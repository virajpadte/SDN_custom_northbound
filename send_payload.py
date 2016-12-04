#!/usr/bin/env python

import MySQLdb
import json

# get json credentials
with open('config.json') as json_data_file:
    data = json.load(json_data_file)
host = data["mysql"]["host"]
user = data["mysql"]["user"]
passwd = data["mysql"]["passwd"]
db_name = data["mysql"]["db"]


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
        grp_list = list()
        #return a list of grps:
        for result in results:
            grp_list.append(result[0])
        print(grp_list)
        return grp_list
    except MySQLdb.Error, e:
        print("exception occured")
        print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
        # Rollback in case there is any error
        db.rollback()
    # disconnect from server
    db.close()


def get_host_ip_list(grp_id):
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
    query = "SELECT ip FROM hosts WHERE group_id=%s"
    try:
        # Execute the SQL command
        cursor.execute(query, (grp_id))
        # Fetch all the rows in a list of lists.
        ip_list = cursor.fetchall()
        ip_list_clean = list()
        # print received data:
        for ip in ip_list:
            ip_list_clean.append(ip[0])
        return ip_list_clean

    except MySQLdb.Error, e:
        print("exception occured")
        print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
        # Rollback in case there is any error
        db.rollback()
    # disconnect from server
    db.close()

def make_payload(ip_list, grp_list, policy_dict):
    payload = {}
    master_grp = {}
    grp_dict_list = []
    for idx, grp in enumerate(grp_list):
        grp = {}
        grp["host_ips"] = ip_list[idx]
        master_grp[grp_list[idx]] = grp
    payload["Groups"] = [master_grp]
    # add policies
    payload["Policy"] = [policy_dict]
    return payload


def update_controller():
    grp_list = get_grps()
    ip_list = list()

    for grp in grp_list:
        # getting a host list for each unique grp
        ip_list_per_grp = get_host_ip_list(grp)
        print(ip_list_per_grp)
        ip_list.append((ip_list_per_grp))
    #populated grp_list
    print(grp_list)
    # populated ip_list
    print(ip_list)
    #generated policy dict
    policy_dict = {"group_isolation": "0", "UDP_packet_restriction": "1"}
    payload = make_payload(ip_list,grp_list,policy_dict)
    json_payload = json.dumps(payload)
    print(json_payload)
    parsed_json = json.loads(json_payload)
    print(parsed_json["Groups"][0]["2"])
    #send payload to all:


if __name__ == "__main__":
    # get json credentials
    with open('config.json') as json_data_file:
        data = json.load(json_data_file)
    host = data["mysql"]["host"]
    user = data["mysql"]["user"]
    passwd = data["mysql"]["passwd"]
    db_name = data["mysql"]["db"]
    update_controller()




