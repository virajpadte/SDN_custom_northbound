import json


def make_payload(ip_list,grp_list,policy_list):
    payload = {}
    master_grp = {}
    grp_dict_list = []
    for idx,grp in enumerate(grp_list):
        grp = {}
        grp["host_ips"] = ip_list[idx]
        #grp["host_ips"] = ip_list[idx]
        #print(grp)
        master_grp[grp_list[idx]] = grp
    payload["Groups"] = [master_grp]
    #add policies
    payload["Policy"] = [policy_list]
    return  payload


if __name__ == "__main__":


    #sample payload--------
    ip1 = '10.10.1.1'
    d = {
    "Policy": [
            {
                "group_isolation": "0",
                "UDP_packet_restriction": "0"
            },
        ],
    "Groups": [
        {
            "Group1": {
                "host_ips": [ip1, '10.10.1.2'],
            },
            "Group2": {
                "host_ips": ['10.10.1.3', '10.10.1.4'],
                }
            },
        ],
    }

    print(d)
    print(d["Groups"][0]["Group1"])
    print(d["Groups"][0]["Group2"])
    #json_payload = json.dumps(d)
    #parsed_json = json.loads(json_payload)
    #print(parsed_json["Groups"][0]["Group1"])

    print("----------   ")
    # data = {}
    # print(type(data))
    #
    #
    # grp_tag = "Groups"
    #
    # Group1_ip_dict = {}
    # ip_list1 = ['10.10.1.1','10.10.1.2']
    # Group1_ip_dict["host_ips"] = ip_list1
    #
    # Group2_ip_dict = {}
    # ip_list2 = ['10.10.1.3', '10.10.1.4']
    # Group2_ip_dict["host_ips"] = ip_list2
    #
    # Group_dict = {}
    # Group_dict["Group1"]= Group1_ip_dict
    # #Group2_dict = {}
    # Group_dict["Group2"] = Group2_ip_dict
    #
    #
    # data[grp_tag] = [Group_dict]
    #
    # print(data)
    # print(data["Groups"][0]["Group1"])
    # print(data["Groups"][0]["Group2"])
    #
    # print("----------   ")

    grp_list = ['Group1','Group2', 'Group3']
    ip_list1 = ['10.10.1.1', '10.10.1.2']
    ip_list2 = ['10.10.1.3', '10.10.1.4']
    ip_list3 = ['10.10.1.5', '10.10.1.6']
    ip_list = [ip_list1, ip_list2, ip_list3]

    #policy list:
    policy_list = {"group_isolation":"0", "UDP_packet_restriction": "1", "No_viraj_packets": "1", "No_saurabh_packets": "0"}
    payload = make_payload(ip_list,grp_list,policy_list)
    print(payload)
    print(payload["Groups"][0]["Group1"])
    print(payload["Groups"][0]["Group2"])
    print(payload["Groups"][0]["Group3"])






