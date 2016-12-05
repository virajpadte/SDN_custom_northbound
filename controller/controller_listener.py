import socket
import sys
import json

#get connection details:
with open('connection_details.json') as json_data_file:
    data = json.load(json_data_file)
ip = data["controller"]["ip"]
port = int(data["controller"]["port"])

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = (ip, port)
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

while True:
    # Wait for a connection
    print >>sys.stderr, 'waiting for a connection'
    connection, client_address = sock.accept()
    # Receive the data in small chunks and retransmit it
    data = connection.recv(1024)
    if data:
        print >>sys.stderr, 'received "%s"' % data
	break
#close connection
connection.close()

#process_data
#--------------------------------------
parsed_json = json.loads(data)
#print(parsed_json["Groups"][0]["2"])
number_of_grps = len(parsed_json["Groups"][0])
print("number_of_grps", number_of_grps)
grp_name_list = parsed_json["Groups"][0].keys() 
print("grp_name_list",grp_name_list)
#parsed_json["Groups"][0].

master_ip_list = list()
for grp in grp_name_list:
    unicode_ip_list = parsed_json["Groups"][0][grp]["host_ips"]
    #print(unicode_ip_list)
    ip_list = map(str, unicode_ip_list)
    #print(ip_list)
    master_ip_list.append(ip_list)
print("master_IP_list",master_ip_list)

def find_grp(master_ip_list,ip):
    for sublist in master_ip_list:
	#print("sublist", sublist)
    	if ip in sublist:
       	   #print "Found it!", sublist
       	   break
    found_grp = master_ip_list.index(sublist)
    return found_grp


print("Found_grp",find_grp(master_ip_list,'10.10.1.1'))

#policy_info_retrive
group_isolation_status = parsed_json["Policy"][0]["group_isolation"]
UDP_packet_restriction = parsed_json["Policy"][0]["UDP_packet_restriction"]
print("group_isolation_status", group_isolation_status)
print("UDP_packet_restriction", UDP_packet_restriction)
#-----------------------------------------
