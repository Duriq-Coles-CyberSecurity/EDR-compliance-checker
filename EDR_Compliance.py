import csv

cmdb_file = "cmdblist.csv" #input().strip() grabs csv from org cmdb
edr_file = "edrlist.csv" #input().strip() grabs edr inventory export
excpt_file = "excptlist.csv" #input().strip() grabs exception list inventory export


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


# opens exception list  sv file, reads it and prints each row
with open(excpt_file, "r") as exf:
    exf_reader = csv.reader(exf)
    next(exf_reader) #skips the header row
    excpt_list = {}
    for row in exf_reader:
        #print(row[0],row[1])
        for i in range(0, len(row)): # grab the host name and then the IP address to stores them in dictionary for cmdb inventory
            key = row[0].strip()
            value = row[1].strip()
            excpt_list[key] = value

cmdb_count = 0 # keeps count of how many do not match in the edr
edr_count = 0  #keeps count of how many in the edr match
excpt_count = 0 #keeps count of how many are on the exception list to substract from the total
missing_edr = {} # empty dictionary for the missing computer in edr

#counts the number of times the host names in the cmdb list match the hostnames in the edr list
for key in cmdb_list.keys():
    if key in edr_list:
        edr_count +=1 # keeps count of how many in the edr match  
    else:
        if cmdb_list[key] in edr_list.values():
            edr_count +=1 # keeps count of how many in the edr match
        else:
            if key in excpt_list:
                excpt_count += 1
                #print(excpt_count, key)
            else:
                if cmdb_list[key] in excpt_list.values():
                    excpt_count += 1
                    #print(excpt_count, key)
                    
                else:
                    cmdb_count += 1 # keeps count of how many do not match in the edr
                    missing_edr[key] = cmdb_list[key] # adds computer with no match from cmdb to edr missing list
                    #print(cmdb_count, key)


#calculated the edr compliance
total_cmdb = edr_count + cmdb_count + excpt_count # total may be lower than expectd due to the logic of the dictionars created depulication entries used for the key and only updated the value used for the IP address if it was different.
print()
print(f'There are {edr_count} out of {total_cmdb} computers from the cmdb in the edr tool')
edr_comply_pt = (edr_count / total_cmdb) * 100  # total computers found within EDR divided by to total edr count + the total cmdb count of computers missing edr then subtracking the total computers found to be exceptions then times 100
print(f'EDR is {edr_comply_pt:.2f}% deployed to all in scope systems in the environment!')
print()
print(f'There are {excpt_count} out of {total_cmdb} computers from the cmdb on the exception list')
excpt_comply_pt = (excpt_count / total_cmdb) * 100  # total computers found within EDR divided by to total edr count + the total cmdb count of computers missing edr then subtracking the total computers found to be exceptions then times 100
print(f'{excpt_comply_pt:.2f}% of the cmdb inventory are expected to be excluded from EDR compliance counts total.')  
print()
print(f'There are {cmdb_count} out of {total_cmdb} computers from the cmdb NOT in the edr tool or the exception list')
missing_comply_pt = (cmdb_count / total_cmdb) * 100  # total computers found within EDR divided by to total edr count + the total cmdb count of computers missing edr then subtracking the total computers found to be exceptions then times 100
print(f'{missing_comply_pt:.2f}% of the cmdb inventory are not expected to be excluded or does not have EDR deployed.')  
print()


miss_edr_file = "missedrlist.csv"

missing = [] #empty list of the all the computer that do not have edr
for key in missing_edr:
    missing.append([key, missing_edr[key]])

with open(miss_edr_file, "w", newline="") as mf:
    mf_writer = csv.writer(mf)
    for i in range (len(missing)):
        mf_writer.writerow(missing[i])

print()
print(f'Here is the list of computers from the CMDB missing EDR: missedrlist.csv')
print()
#print(len(missing))

#this is for debugging the missing edr list csv not being created properly
'''
with open(miss_edr_file, "r") as mf:
    mf_reader = csv.reader(mf)
    for row in mf_reader:
        print(row)
'''

