import csv

FILE = './data.csv'
HEADERS = ['S/N','CONTACT_NAME','GSM1','NO1','GSM2','NO2']
ATTRIBUTES = HEADERS[1:]
NETWORKS = ['AIRTEL','MTN','GLO']
dummy_data = [
    ['Mum','AIRTEL','08091234322',None,None],
    ['Dad','MTN','09122345794',None,None]
]

def get_contacts():
    global FILE
    global HEADERS
    contacts = []
    with open(FILE,mode='r',encoding='utf-8') as f:
        reader = csv.reader(f)
        contacts = list(reader)
        return contacts
#       reader = csv.DictReader(f)
#        for row in reader:
#           name = row.get(HEADERS[0])
#           gsm1 = row.get(HEADERS[1])
#           gsm2 = row.get(HEADERS[3])
#           no1 = row.get(HEADERS[2])
#           no2 = row.get(HEADERS[4])           
#           single_row = [name,gsm1,no1,gsm2,no2]
#           contacts.append(single_row)
#   return contacts
                     

def print_contacts() -> None:
    global FILE
    global HEADERS
    contacts = {}
    with open(FILE,mode='r',encoding='utf-8') as f:
        reader = csv.DictReader(f)

        print(f'S/N\t|\tNames\t|\tNETWORK\t|\tNUMBERS_1\t|\tNETWORK_2\t|\tNUMBERS_2')

        for row in reader:
            sn = row.get(HEADERS[0])
            name = row.get(HEADERS[1])
            gsm1 = row.get(HEADERS[2])
            gsm2 = row.get(HEADERS[4])
            no1 = row.get(HEADERS[3])
            no2 = row.get(HEADERS[5])
            # validating if entry attributes exist
            no2 = 'Unavailable Number' if (len(no2) < 1) else no2
            gsm2 = 'Undefined Network' if (len(gsm2) < 1) else gsm2

            print(f'{sn}\t|{name}\t|{gsm1}\t|{no1}\t|{gsm2}\t|{no2}')


def update_contact(
        *,#kwargs
        serial:int,
        attr_id:int,#get the position of selected attr in list
        new_val:str
    ):
    global FILE
    global HEADERS
    
    if not serial or type(serial) != type(1):
        raise ValueError('missing or invalid serial no of contact')
        return 

    total_data = []
    current_data = get_contacts()
    for inner_list in current_data:
        total_data.append(inner_list)
        
    if attr_id < 1 or attr_id > 5:
        raise IndexError('attribute ID outside range of 1 - 5')
        return

    total_data[serial][attr_id] = new_val
    #print(total_data)
    with open(FILE,mode='w',newline='',encoding='utf-8') as f:
        writer = csv.writer(f)
        # headers
        writer.writerow(HEADERS)
        # add edited data
        writer.writerows(total_data[1:])

        return total_data[serial]


def add_contact(
    contact_name:str,
    gsm1:str,
    no1:str,
    gsm2=None,
    no2=None
    ) -> None:
    global FILE
    
    serial = [get_serial() + 1]
    with open(FILE,mode='a',newline='',encoding='utf-8') as f:
        writer = csv.writer(f)
        new_entry = [contact_name,gsm1,no1,gsm2,no2]
        writer.writerow(serial + new_entry)

    
def populate_data():
    global FILE
    global HEADERS
    
    is_head = False
    serial_ctr = [get_serial()]
    with open(FILE,mode='r',newline='',encoding='utf-8') as f:
        rdr = csv.reader(f)
        every = list(rdr)
        if len(every) >= 1: 
            if every[0] == HEADERS:
                is_head = True


    with open(FILE,mode='a',newline='',encoding='utf-8') as f:

        writer = csv.writer(f)

        # define file headers(uses list) if not there
        if not is_head:
            writer.writerow(HEADERS)
        # populate data store
        serial_ctr[0] += 1#for first new entry
        for entry in dummy_data:
            writer.writerow(serial_ctr + entry)
            serial_ctr[0] += 1


def get_serial():
    global FILE
    global HEADERS
    serial_no = 0
    with open(FILE,mode='r',newline='',encoding='utf-8') as f:
        reader = csv.reader(f)
        data_list = list(reader)
        if len(data_list) >= 1:
            #more validation could be added to check if the header is actually the first row of the file
            if data_list[0] == HEADERS:
                serial_no = len(data_list[1:])

    return serial_no

def delete_contact(*,serial:int):
    global FILE
    global HEADERS

    all_data = []
    del_contact = None
    current_data = get_contacts()
    # refill container list without selected one to delete
    for contact in current_data[1:]:
        if int(contact[0]) != serial:
            all_data.append(contact)
        else:
            #print(contact)
            del_contact = contact

    # remove serial numbers from each entry
    trunc_data = []
    for rem_data in all_data:
        trunc_data.append(rem_data[1:])

    #print(trunc_data)

    # time to update data store
    serial_ctr = [1]

    with open(FILE,mode='w',newline='',encoding='utf-8') as f:
        wtr = csv.writer(f)
        # headers
        wtr.writerow(HEADERS)
        # rest
        for data in trunc_data:
            wtr.writerow(serial_ctr + data)
            serial_ctr[0] += 1

    return del_contact

def get_contact(serial:int):
    all_contacts = get_contacts()
    return all_contacts[serial]
    


#if __name__ == '__main__':
    #populate_data()
    #print(get_serial())
    #print_contacts()
    #print(get_contacts())
    #add_contact('aunt B','MTN','081770542281')
    #update_contact(serial=2,attr_id=4,new_val='AIRTEL')
    #delete_contact(serial=1)
    #print(get_contact(2))
    
