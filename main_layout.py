from Tkinter import *
import ttk
import MySQLdb
import json
import socket
import send_payload


class MainView:
    def __init__(self, master):
        self.master = master

        mainframe = ttk.Frame(self.master, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        mainframe.columnconfigure(0, weight=1)
        mainframe.rowconfigure(0, weight=1)

        ttk.Label(mainframe, text="Hosts").grid(column=1, row=1, sticky=W)
        ttk.Button(mainframe, text="Add Host", command=self.add_host_window).grid(column=2, row=1, sticky=W)

        ttk.Button(mainframe, text="Modify Host", command=self.modify_window).grid(column=3, row=1, sticky=W)
        ttk.Button(mainframe, text="Delete Host", command=self.delete_window).grid(column=4, row=1, sticky=W)

        ttk.Label(mainframe, text="Groups").grid(column=1, row=4, sticky=W)
        ttk.Button(mainframe, text="View Group", command=self.view_window).grid(column=2, row=4, sticky=W)

        ttk.Label(mainframe, text="Policies").grid(column=1, row=6, sticky=W)
        ttk.Button(mainframe, text="Enforce Policy", command=self.enforce_window).grid(column=2, row=6, sticky=W)
        ttk.Button(mainframe, text="View Policy", command=self.view_poly_window).grid(column=3, row=6, sticky=W)

        for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

    def add_host_window(self):
        print("add_host_outer")
        self.newWindow = Toplevel(root)
        self.app = Create_host(self.newWindow)

    def modify_window(self):
        print("modify")
        self.newWindow = Toplevel(root)
        self.app = Modify_host(self.newWindow)

    def delete_window(self):
        print("delete")
        self.newWindow = Toplevel(root)
        self.app = Delete_host(self.newWindow)

    def view_window(self):
        print("view")
        self.newWindow = Toplevel(root)
        self.app = View_group(self.newWindow)

    def enforce_window(self):
        print("enforce")
        self.newWindow = Toplevel(root)
        self.app = Enforce_policy(self.newWindow)

    def view_poly_window(self):
        print("view_poly")
        self.newWindow = Toplevel(root)
        self.app = View_policy(self.newWindow)


class Create_host:
    def __init__(self, master):
        self.master = master
        self.master.title("Create a host")
        mainframe = ttk.Frame(self.master, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        mainframe.columnconfigure(0, weight=1)
        mainframe.rowconfigure(0, weight=1)

        GROUP = StringVar()
        HOST = StringVar()
        IP = StringVar()
        #PORT = StringVar()
        # status = StringVar()

        ttk.Label(mainframe, text="Create host").grid(column=1, row=1, sticky=W)

        ttk.Label(mainframe, text="GROUP ID").grid(column=1, row=2, sticky=W)
        GROUP_ID_entry_box = ttk.Entry(mainframe, width=39, textvariable=GROUP)
        GROUP_ID_entry_box.grid(column=2, row=2, sticky=W)

        ttk.Label(mainframe, text="HOST ID").grid(column=1, row=3, sticky=W)
        HOST_ID_entry_box = ttk.Entry(mainframe, width=39, textvariable=HOST)
        HOST_ID_entry_box.grid(column=2, row=3, sticky=W)

        ttk.Label(mainframe, text="IP Address").grid(column=1, row=4, sticky=W)
        IP_entry_box = ttk.Entry(mainframe, width=39, textvariable=IP)
        IP_entry_box.grid(column=2, row=4, sticky=W)

        #ttk.Label(mainframe, text="PORT").grid(column=1, row=5, sticky=W)
        #PORT_entry_box = ttk.Entry(mainframe, width=39, textvariable=PORT)
        #PORT_entry_box.grid(column=2, row=5, sticky=W)

        ttk.Button(mainframe, text="Save", command=lambda: self.add_host(GROUP, HOST, IP)).grid(column=2, row=6,
                                                                                                      sticky=W)
        # ttk.Label(mainframe, textvariable=status).grid(column=2, row=6, sticky=E, padx=50)

        for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

    def add_host(self, grp_id, host_id, ip):
        try:
            print("add_host_inner")
            # check_connection()
            GROUP_ID = grp_id.get()
            host_id = host_id.get()
            ip = ip.get()
            #port = port.get()
            print("GROUP_ID", GROUP_ID)
            print("HOST_ID", host_id)
            print("IP_ADDRESS", ip)
            #print("PORT", port)
            self.new_host(GROUP_ID, host_id, ip)
        except ValueError:
            pass

    def new_host(self, grp_id, host_id, ip):
        # Open database connection
        db = MySQLdb.connect(host, user, passwd, db_name)
        # testing connection:
        if db.open:
            print("connection is established")
        else:
            print("could not establish connection. Check credentials or connects sysops admin")
        # prepare a cursor object using cursor() method
        cursor = db.cursor()
        # CREATE SQL QUERY:
        query = """INSERT INTO hosts(host_id, ip, group_id) VALUES (%s,%s,%s)"""
        try:
            # Execute the SQL command
            cursor.execute(query, (host_id, ip, grp_id))
            # Commit your changes in the database
            db.commit()
            # debug print:
            print("data inserted in the db table")
        except MySQLdb.Error, e:
            print("exception occured")
            print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
            # Rollback in case there is any error
            db.rollback()
        # disconnect from server
        db.close()
        #send updates
        send_payload.update_controller()
        self.master.destroy()


class Modify_host:
    def __init__(self, master):
        self.master = master
        self.master.title("Modify existing host")
        mainframe = ttk.Frame(self.master, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        mainframe.columnconfigure(0, weight=1)
        mainframe.rowconfigure(0, weight=1)

        GROUP_ID = StringVar()
        HOST_ID = StringVar()
        ttk.Label(mainframe, text="Modify host").grid(column=1, row=1, sticky=W)
        ttk.Label(mainframe, text="HOST ID").grid(column=1, row=2, sticky=W)
        HOST_ID_entry_box = ttk.Entry(mainframe, width=39, textvariable=HOST_ID)
        HOST_ID_entry_box.grid(column=2, row=2, sticky=W)
        ttk.Label(mainframe, text="GROUP ID").grid(column=1, row=3, sticky=W)
        GROUP_ID_entry_box = ttk.Entry(mainframe, width=39, textvariable=GROUP_ID)
        GROUP_ID_entry_box.grid(column=2, row=3, sticky=W)
        ttk.Button(mainframe, text="Modify", command=lambda: self.modify_host(HOST_ID, GROUP_ID)).grid(column=2, row=6,
                                                                                                       sticky=W)
        for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

    def modify_host(self, host_id, grp_id):
        try:
            # check_connection()
            grp_id = grp_id.get()
            host_id = host_id.get()
            print("HOST_id", host_id)
            print("GROUP_ID", grp_id)
            self.update_groups(grp_id, host_id)
        except ValueError:
            pass

    def update_groups(self, grp_id, host_id):
        # Open database connection
        db = MySQLdb.connect(host, user, passwd, db_name)
        # testing connection:
        if db.open:
            print("connection is established")
        else:
            print("could not establish connection. Check credentials or connects sysops admin")
        # prepare a cursor object using cursor() method
        cursor = db.cursor()
        # CREATE SQL QUERY:
        query = """UPDATE hosts SET group_id=%s WHERE host_id=%s"""
        try:
            # Execute the SQL command
            cursor.execute(query, (grp_id, host_id))
            # Commit your changes in the database
            db.commit()
            # debug print:
            print("data updated in the db table")
        except MySQLdb.Error, e:
            print("exception occured")
            print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
            # Rollback in case there is any error
            db.rollback()
        # disconnect from server
        db.close()
        #send updates
        send_payload.update_controller()
        self.master.destroy()


class Delete_host:
    def __init__(self, master):
        self.master = master
        self.master.title("Delete a host")
        mainframe = ttk.Frame(self.master, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        mainframe.columnconfigure(0, weight=1)
        mainframe.rowconfigure(0, weight=1)
        HOST_ID = StringVar()
        ttk.Label(mainframe, text="Delete host").grid(column=1, row=1, sticky=W)
        ttk.Label(mainframe, text="HOST ID").grid(column=1, row=2, sticky=W)
        HOST_ID_entry_box = ttk.Entry(mainframe, width=39, textvariable=HOST_ID)
        HOST_ID_entry_box.grid(column=2, row=2, sticky=W)
        ttk.Button(mainframe, text="Delete", command=lambda: self.delete_host(HOST_ID)).grid(column=2, row=6, sticky=W)
        for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

    def delete_host(self, host_id):
        try:
            # check_connection()
            host_id = host_id.get()
            print("HOST_id", host_id)
            self.delete_host_entry(host_id)
        except ValueError:
            pass

    def delete_host_entry(self, host_id):
        # Open database connection
        db = MySQLdb.connect(host, user, passwd, db_name)
        # testing connection:
        if db.open:
            print("connection is established")
        else:
            print("could not establish connection. Check credentials or connects sysops admin")
        # prepare a cursor object using cursor() method
        cursor = db.cursor()
        # CREATE SQL QUERY:
        query = """DELETE FROM hosts WHERE host_id=%s"""
        try:
            # Execute the SQL command
            cursor.execute(query, (host_id,))
            # Commit your changes in the database
            db.commit()
            # debug print:
            print("data removed from the db table")
        except MySQLdb.Error, e:
            print("exception occured")
            print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
            # Rollback in case there is any error
            db.rollback()
        # disconnect from server
        db.close()
        #send updates
        send_payload.update_controller()
        self.master.destroy()


class View_group:
    def __init__(self, master):
        self.master = master
        self.master.title("View a host group")
        mainframe = ttk.Frame(self.master, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        mainframe.columnconfigure(0, weight=1)
        mainframe.rowconfigure(0, weight=1)
        GROUP_ID = StringVar()
        ttk.Label(mainframe, text="ENTER GROUP ID").grid(column=1, row=1, sticky=W)
        GROUP_ID_entry_box = ttk.Entry(mainframe, width=39, textvariable=GROUP_ID)
        GROUP_ID_entry_box.grid(column=1, row=2, sticky=W)

        lbox = Listbox(mainframe, height=6, width=50)
        lbox.grid(column=1, row=4, rowspan=6, sticky=(N, S, E, W))

        # results = ('Argentina', 'Australia', 'Belgium', 'Brazil', 'Canada', 'China')
        # for result in results:
        #    lbox.insert(END, result)

        ttk.Button(mainframe, text="Populate", command=lambda: self.view_hosts(GROUP_ID, lbox)).grid(column=1, row=3,
                                                                                                     sticky=W)
        for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

    def view_hosts(self, grp_id, listbox_widget):
        try:
            # check_connection()
            grp_id = grp_id.get()
            print("GRP_ID", grp_id)
            results = self.fetch_data(grp_id)
            # referesh content of the list box
            # clearing all content:
            listbox_widget.delete(0, END)
            # adding new content:
            if not len(results):
                listbox_widget.insert(END, "NO HOSTS ASSOCIATED WITH PROVIDED GROUP ID")
            else:
                listbox_widget.insert(END, "HOST ID" + "              " + "GROUP ID")
                for result in results:
                    listbox_widget.insert(END, result[0] + " -------------> " + result[1])
                # Colorize alternating lines of the listbox:
                for i in range(0, len(results), 2):
                    listbox_widget.itemconfigure(i, background='#f0f0ff')
        except ValueError:
            pass

    def fetch_data(self, grp_id):
        # Open database connection
        db = MySQLdb.connect(host, user, passwd, db_name)
        # testing connection:
        if db.open:
            print("connection is established")
        else:
            print("could not establish connection. Check credentials or connects sysops admin")
        # prepare a cursor object using cursor() method
        cursor = db.cursor()
        # CREATE SQL SELECT QUERY:
        query = """SELECT host_id,group_id FROM hosts WHERE group_id=%s"""
        try:
            # Execute the SQL command
            cursor.execute(query, (grp_id,))
            # Fetch all the rows in a list of lists.
            results = cursor.fetchall()
            for row in results:
                print(row)
            print("Fetched all data")
            return results
        except MySQLdb.Error, e:
            print("exception occured")
            print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
            # Rollback in case there is any error
            db.rollback()
        # disconnect from server
        db.close()
        self.master.destroy()


class Enforce_policy:
    def __init__(self, master):
        self.master = master
        self.master.title("View a host group")
        mainframe = ttk.Frame(self.master, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        mainframe.columnconfigure(0, weight=1)
        mainframe.rowconfigure(0, weight=1)
        HOST_ID = StringVar()
        grp_iso_status = StringVar()
        restrc_status = StringVar()
        #default values:
        grp_iso_status.set("0")
        restrc_status.set("0")

        ttk.Label(mainframe, text="Select policy").grid(column=1, row=1, sticky=W)
        grp_iso = ttk.Radiobutton(mainframe, text='group isolation', variable=grp_iso_status, value="1")
        restrc = ttk.Radiobutton(mainframe, text='UDP packet restriction', variable=restrc_status, value="1")
        grp_iso.grid(column=1, row=2, sticky=W, padx=20)
        restrc.grid(column=1, row=3, sticky=W, padx=20)
        ttk.Button(mainframe, text="Apply policy", command=lambda: self.enforce_policy(grp_iso_status,restrc_status)).grid(column=1, row=4,
                                                                                               sticky=W)

        for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

    def enforce_policy(self,grp_iso_status,restrc_status):
        try:
            print("enforced")
            #check_connection()
            grp_iso_status = grp_iso_status.get()
            restrc_status = restrc_status.get()
            print("isolation status", grp_iso_status)
            print("restriction status", restrc_status)
            self.update_policy(grp_iso_status,restrc_status)
        except ValueError:
            pass

    def update_policy(self,grp_iso_status,restrc_status):
        # Open database connection
        db = MySQLdb.connect(host, user, passwd, db_name)
        # testing connection:
        if db.open:
            print("connection is established")
        else:
            print("could not establish connection. Check credentials or connects sysops admin")
        # prepare a cursor object using cursor() method
        cursor = db.cursor()

        #check if db is empty:
        try:
            #test SQL query
            query = """SELECT * FROM POLICY"""
            # Execute the SQL command
            cursor.execute(query)
            # Fetch all the rows in a list of lists.
            test_entry = cursor.fetchone()
            if not len(test_entry):
                query = """INSERT INTO POLICY(grp_iso, udp_pck_restr) VALUES ( %s, %s)"""
            else:
                query = """UPDATE POLICY SET grp_iso=%s,udp_pck_restr=%s WHERE id=%s"""
            # Execute the SQL command
            cursor.execute(query, (grp_iso_status, restrc_status, "1"))
            # Commit your changes in the database
            db.commit()
            # debug print:
            print("data inserted/updated in the db table")
        except MySQLdb.Error, e:
            print("exception occured")
            print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
            # Rollback in case there is any error
            db.rollback()
        # disconnect from server
        db.close()
        #send updates
        send_payload.update_controller()
        self.master.destroy()

class View_policy:
    def __init__(self, master):
        self.master = master
        self.master.title("View a host group")
        mainframe = ttk.Frame(self.master, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        mainframe.columnconfigure(0, weight=1)
        mainframe.rowconfigure(0, weight=1)
        ttk.Label(mainframe, text="View policy in use:").grid(column=1, row=1, sticky=W)



        group_iso_status = StringVar()
        packet_rest_status = StringVar()


        #get status:
        # Open database connection
        db = MySQLdb.connect(host, user, passwd, db_name)
        # create db cursor
        cursor = db.cursor()
        try:
            #test SQL query
            query = """SELECT grp_iso, udp_pck_restr FROM POLICY"""
            cursor.execute(query)
            # Fetch all the rows in a list of lists.
            status = cursor.fetchone()
            print("status", status)
            if status[0] == 0 and status[1] == 0:
                group_iso_status.set("GROUP ISOLATION POLICY - NOT ACTIVATED")
                packet_rest_status.set("UDP PACKET RESTRICTION POLICY - NOT ACTIVATED")
            elif status[0] == 1 and status[1] == 0:
                group_iso_status.set("GROUP ISOLATION POLICY - ACTIVATED")
                packet_rest_status.set("UDP PACKET RESTRICTION POLICY - NOT ACTIVATED")
            elif status[0] == 0 and status[1] == 1:
                group_iso_status.set("GROUP ISOLATION POLICY - NOT ACTIVATED")
                packet_rest_status.set("UDP PACKET RESTRICTION POLICY - ACTIVATED")
            else:
                group_iso_status.set("GROUP ISOLATION POLICY - ACTIVATED")
                packet_rest_status.set("UDP PACKET RESTRICTION POLICY - ACTIVATED")

            ttk.Label(mainframe, text=group_iso_status.get()).grid(column=1, row=2, sticky=W)
            ttk.Label(mainframe, text=packet_rest_status.get()).grid(column=1, row=3, sticky=W)
        except MySQLdb.Error, e:
            print("exception occured")
            print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
            # Rollback in case there is any error
            db.rollback()
        db.close()
        for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)



if __name__ == "__main__":
    # get json credentials
    with open('config.json') as json_data_file:
        data = json.load(json_data_file)
    host = data["mysql"]["host"]
    user = data["mysql"]["user"]
    passwd = data["mysql"]["passwd"]
    db_name = data["mysql"]["db"]

    root = Tk()
    root.title("Policy Manager")
    main = MainView(root)
    root.mainloop()
