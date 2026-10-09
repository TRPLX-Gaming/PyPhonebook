import files as ff
from config import LOCAL

flag = True

def start(phase=0) -> None:
    global flag

    if phase == 0:
        print('welcome to my phonebook')
        # choose mode for validation
        mode = input('What is your location?\n Y=Nigeria\n N=Other\nNigeria is enabled by default\nYour location: ')
        if yes_or_no(mode):
            LOCAL = True
        else:
            LOCAL = False


    elif phase == 1:
        again = input('do you have another operation you want to do?(y/n)\nAnswer: ').lower().strip()
        if yes_or_no(again):
            flag = True
        else:
            flag = False
            print('thanks for using my program!')
            return


    while flag:
        stage_pick = input('What do you wanna do today!\n- A. Read phonebook contents.\n- B. Add new contact to phonebook.\n- C. Update existing contact in phonebook.\n- D. delete a contact from phonebook\n- E. exit program.\n \nPick your operation by typing the letters preceeding them\nYour pick: ').lower().strip()
        
        match stage_pick:
            case 'a':
                list_all()
                start(1)
                break
            case 'b':
                add_new()
                start(1)
                break
            case 'c':
                update()
                start(1)
                break
            case 'd':
                delete()
                start(1)
                break
            case 'e':
                print('Goodbye...for now.')
                flag = False
                return
            case _:
                print('invalid input, select again')
                start(0)
                    
        

def yes_or_no(response:str) -> bool:
    try:
        res = response.lower().strip()
        if res is None:
            raise InvalidInputError('err occured due to invalid input')

        if res == 'y' or res == 'yes':
            return True
        return False
    except Exception as e:
        print(f'err occured: {e}')


def list_all():
    check = ff.get_contacts()
    if len(check[1:]) < 1:
        print('no contacts saved so far...')
        return

    ff.print_contacts()
    return 1

def add_new():
    print('fill in necessary info, just press Enter if you choose to leave a fied blank')
    name = input_cleaner(input('name of contact: '))
    fir_gsm = input_cleaner(input('telecommunication network: '))
    fir_num = input_cleaner(input('first GSM number: '))
    sec_gsm = input_cleaner(input('2nd telecommunication network: '))
    sec_num = input_cleaner(input('2nd GSM number: '))

    new = [name, fir_gsm, fir_num, sec_gsm, sec_num]
    ff.add_contact(name,fir_gsm,fir_num,sec_gsm,sec_num)
    print(f'new contact added: {new}')

def update():
    print('select the serial number of the contact that you want to modify')
    if list_all() == None:
        print('no contacts to modify')
        return

    sn = int(input('contact serial number: '))
    attr = int(input('Select which attribute you want to modify:\n- 1. Contact Name\n- 2. First GSM Network\n- 3. First GSM Number\n- 4. Second GSM Network\n- 5. Second GSM Number\n\nYour pick(in number): '))
    new = input('The new data to replace the old one: ').strip()
    
    old = ff.get_contact(sn)
    print(f'old -----> {old}')

    newer = ff.update_contact(serial=sn, attr_id=attr, new_val=new)
    print(f'new -----> {newer}')


def delete():
    print('select what contact you want to delete by serial number')
    list_all()
    sn = int(input('contact serial number to delete: '))
    deleted = ff.delete_contact(serial=sn)
    print(f'deleted contact ----> {deleted}')
    print('updated phonebook')
    list_all()

def input_cleaner(val:str) -> str | None:
    try:
        if len(val) > 1:
            return val.lower().strip()
        else:
            return None
    except Exception as e:
        print(f'err occured while formatting string.\nReason: {e}')


# testing custom err
class InvalidInputError(Exception):
    pass

start()
