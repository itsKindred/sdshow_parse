#!/usr/bin/env python3

import sys
import re

C_RED="\033[1;31m"
C_RESET = "\033[0m"
C_YELLOW="\033[1;33m"
C_WHITE="\033[1;37m"

rightsMappings = { "CC": "QUERY_CONFIG", "DC": C_RED + "CHANGE_CONFIG" + C_RESET, "LC": "QUERY_STATS", "SW": "ENUM_DEPENDENCIES", "RP": C_YELLOW + "START_SERVICE" + C_RESET, 
                   "WP": C_YELLOW + "STOP_SERVICE" + C_RESET, "DT": "PAUSE_SERVICE", "LO": "INTERROGATE_SERVICE", "CR": "USER_DEFINED", "GA": "GENERIC_ALL", "GW": "GENERIC_WRITE", 
                   "GR": "GENERIC_READ", "SD": C_YELLOW + "DELETE_SERVICE" + C_RESET, "RC": "READ_CONTROL", "WD": C_RED + "WRITE_DAC" + C_RESET, "WO": C_RED + "WRITE_OWNER" + C_RESET }

userMappings = { "DA": "Domain Administrators", "DG": "Domain Guests", "DU": "Domain Users", "ED": "Enterprise Domain Controllers", "DD": "Domain Controllers", 
                 "DC": "Domain Computers", "BA": "Built-In Administrators", "BG": "Built-In Guests", "BU": "Built-In Users", "LA": "Local Administrator",
                 "LG": "Local Guest Account", "AO": "Account Operators", "BO": "Backup Operators", "PO": "Printer Operators", "SO": "Server Operators",
                 "AU": "Authenticated Users", "PS": "Personal Self", "CO": "Creator Owner", "CG": "Creator Group", "SY": "Local System", "PU": "Power Users",
                 "WD": "Everyone", "RE": "Replicator", "IU": "Interactive Logon User", "NU": "Network Logon User", "SU": "Service Logon User", "RC": "Restricted Code",
                 "WR": "Write Restricted Code", "AN": "Anonymous Logon", "SA":  "Schema Administrators", "CA": "Certificate Services Administrators",
                 "RS": "Remote Access Servers Group", "EA": "Enterprise Administrators", "PA": "Group Policy Administrators", "RU": "Previous Win2000",
                 "LS": "Local Service Account", "NS": "Network Service Account", "RD": "Remote Desktop Users", "NO": "Network Configuration Operators",
                 "MU": "Performance Monitor Users", "LU": "Performance Log Users", "IS": "Anonymous Interner Users", "CY": "Crypto Operators", "OW": "Owner Rights SID",
                 "RM": "RMS Service" }
                  

class sddlString:

    def __init__(self, full_acl):
        self.full_acl = full_acl
        self.acl_entries = []
        self.parseFullString()


    def parseFullString(self):

        sddl_list = self.full_acl.split("(")[1:]
        for i in range(len(sddl_list)):
            sddl_list[i] = sddl_list[i][0:-1]


        for sddl in sddl_list:
            self.parseSddl(sddl)


    def parseSddl(self, sddl):

        sddl_data_dict = {   "ace_type" : None,
                             "ace_flags" : None,
                             "rights" : None,
                             "object_guid" : None,
                             "inherit_object_guid" : None,
                             "resource_attr" : None,
                         }
        
        sddl_dat = sddl.split(";")
        sddl_data_dict["ace_type"] = sddl_dat[0]
        sddl_data_dict["ace_flags"] = sddl_dat[1] #ignored for now
        sddl_data_dict["rights"] = self.parseRights(sddl_dat[2])

        if sddl_dat[5] not in userMappings.keys():
            sddl_data_dict["resource_attr"] = sddl_dat[5] #ignored for now
        else:
            sddl_data_dict["resource_attr"] = userMappings[sddl_dat[5]] 

        sddl_data_dict["inherit_object_guid"] = sddl_dat[4] #ignored for now
        sddl_data_dict["object_guid"] = sddl_dat[3]

        self.acl_entries.append(sddl_data_dict)


    def parseRights(self, rightsString):

        rights = []
        rightsSym = re.findall('..', rightsString)

        for r in rightsSym:
            rights.append(rightsMappings[r])

        return rights

    def display(self):

        for entry in self.acl_entries:
            print("")
            print(C_WHITE + entry["resource_attr"] + C_RESET)
            print("---------------------------------")
            for i in entry["rights"]:
                print(i)
            print("---------------------------------")



if len(sys.argv) == 2:
    sd_string = sddlString(sys.argv[1])
    out = sd_string.display()
else:
    strInput = raw_input("Please input your SDDL String: ")
    sd_string = sddlString(strInput)
    out = sd_string.display()

print("")
print(C_RED + "RED_HIGHLIGHT" + C_RESET + " = FULL CONTROL")
print(C_YELLOW + "YELLOW_HIGHLIGHT" + C_RESET + " = HIGH CONTROL")
print("")
print("")
    



