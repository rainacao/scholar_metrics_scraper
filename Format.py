from bs4 import BeautifulSoup
import requests
import csv
import os
import numpy as np

PATH_TO_DMCBH_MEMBERS_CSV = "Copy of DMCBH member IRP categories_Aug2023.csv"

def filter_for_gs(member_arr):
    gs_member_mask = [int(member_arr[i][8]) for i in range(len(member_arr))]
    gs_member_arr = [member_arr[i] for i in range(len(member_arr)) if gs_member_mask[i] == 1]
    print(f"filtered from {len(member_arr)} members to {len(gs_member_arr)} members based on google scholar profile")
    return gs_member_arr
    

def get_irp_participation(colnum, cols, member_array):
    print(f"getting members of {cols[colnum]} IRP...")
    irp_members = []
    for member_row in member_array:

        # firstname = member_row[1].strip()
        # lastname = member_row[0].strip()
        # search = f"{firstname} {lastname}"
        
        if member_row[10] != "":
            #find using ID and force include
            # print("adding ID")
            search = member_row[10]
        else:
            #find using name
            firstname = member_row[1].strip()
            lastname = member_row[0].strip()
            search = f"{firstname} {lastname}"

        irp_participation = member_row[colnum].strip()
        if irp_participation == "Primary":
            irp_members.append(search)

    # irp_members = [member_names[i] for i in range(len(member_names)) if member_array[i][colnum].strip() == "Primary"]
    print(irp_members)
    print(f"{cols[colnum]} has {len(irp_members)} members\n")

    out_path = f"{cols[colnum]} IRP Members.csv"
    # out_path = f"{cols[colnum]}-simplified.csv"
    with open(out_path, "w+") as f:
        # w = csv.writer(f)
        for member in irp_members:
            f.write(member+"\n")

def format():
    member_arr = []
    with open(PATH_TO_DMCBH_MEMBERS_CSV, "r") as f:
        r = csv.reader(f)
        for row in r:
            if row[0] != "":
                member_arr.append(row)

    # skip header rows
    member_arr = member_arr[2:]
    print(len(member_arr))

    # filter for google scholar
    member_arr = filter_for_gs(member_arr)
    print(len(member_arr))

    # columns of the DMCBH CSV file
    cols = ['Last Name','First Name','Member Type','Mental Health & Addictions','Brain Development & Neurodevelopmental Disorders','Learning Memory & Dementias','Sensory Motor Systems & Movement Disorders','Brain Injury & Repair','Google Scholar?','GS Link']

    # output IRP
    for i in range(3,8):
        get_irp_participation(i, cols, member_arr)

if __name__ == "__main__":
    format()