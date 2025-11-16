import csv

cmdb_file = "cmdblist.csv" #input().strip() grabs csv from org cmdb
edr_file = "edrlist.csv" #input().strip() grabs edr inventory export


# opens cmdb csv file, reads it and prints each row
with open(cmdb_file, "r") as cf:
    cf_reader = csv.reader(cf)
    next(cf_reader) #skips the header row
    cmdb_list = {}
    for row in cf_reader:
        #print(row[0],row[1])
        for i in range(0, len(row)): # grab the host name and then the IP address to stores them in dictionary for cmdb inventory
            key = row[0].strip()
            value = row[1].strip()
            cmdb_list[key] = value
    #print(cmdb_list)

    
# opens edr csv file, reads it and prints each row
with open(edr_file, "r") as ef:
    ef_reader = csv.reader(ef)
    next(ef_reader) #skips the header row
    edr_list = {}
    for row in ef_reader:
        #print(row[0],row[1])

        for i in range(0, len(row)): # grab the host name and then the IP address to stores them in dictionary for edr inventory
            key = row[0].strip()
            value = row[1].strip()
            edr_list[key] = value
    #print(edr_list)

cmdb_count = 0 # keeps count of how many do not match in the edr
edr_count = 0  #keeps count of how many in the edr match
missing_edr = {} # empty dictionary for the missing computer in edr

#counts the number of times the host names in the cmdb list match the hostnames in the edr list
for key in cmdb_list.keys():
    if key in edr_list:
        edr_count +=1 # keeps count of how many in the edr match
          
    else:
        if  cmdb_list[key] in edr_list.values():
            edr_count +=1 # keeps count of how many in the edr match
        else:
            cmdb_count += 1 # keeps count of how many do not match in the edr
            missing_edr[key] = cmdb_list[key] # adds computer with no match from cmdb to edr


print(f'There are {edr_count} computers from the cmdb in the edr tool')
print(f'There are {cmdb_count} computers from the cmdb NOT in the edr tool')

#calculated the edr compliance
comply_pt = (edr_count / (edr_count + cmdb_count)) * 100 
print()
print(f'EDR is {comply_pt:.2f}% deployed to all systems in the environment!')  
 


miss_edr_file = "missedrlist.csv"

missing = [] #empty list of the all the computer that do not have edr
for key in missing_edr:
    missing.append([key, missing_edr[key]])

with open(miss_edr_file, "w", newline="") as mf:
    mf_writer = csv.writer(mf)
    for i in range (len(missing)):
        mf_writer.writerow(missing[i])

print()
print(f'Here is the list of computers from the CMDB missing EDR:')
print()
#print(len(missing))
with open(miss_edr_file, "r") as mf:
    mf_reader = csv.reader(mf)
    for row in mf_reader:
        print(row)

