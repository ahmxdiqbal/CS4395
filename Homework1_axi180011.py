import sys
import csv
import re
import pickle

if sys.argv[1] != "data/data.csv":                                      # making sure datapath is given
    print("error. must pass data path data/data.csv as argument")
    exit()

filepath = sys.argv[1]

class Person:
    last = None
    first = None
    mi = None
    id = None
    phone = None

    def __init__(self, last, first, mi, id, phone):
        self.last = last
        self.first = first
        self.mi = mi
        self.id = id
        self.phone = phone

    def display(self):
        print("Employee iD: " + self.id)
        print("\t" + self.first + " " + self.mi + " " + self.last)
        print("\t" + self.phone)


def process_file(filepath):
    with open(filepath, 'r') as file:
        reader = csv.reader(file)
        rows = list(reader)
        del rows[0]                                             # deleting the first row

        persons_dict = {}

        for row in rows:
            temp = str(row)
            temp = temp[1:len(temp) - 1] 
            last, first, mi, id, phone = temp.split(",")

            last = last[1:len(last) - 1]                        # capitalizing last name and removing quotes
            last = last.capitalize()

            first = first[2:len(first) - 1]                     # capitalizing first name and removing quotes
            first = first.capitalize()

            mi = mi[2:3]                                        # capitalizing initial and removing quotes
            mi = mi.capitalize()
            if mi == "\'":
                mi = "X"

            id = id[2:len(id) - 1]                              # removing quotes and making sure ID is valid
            if check_id(id) == False:
                while check_id(id) == False:
                    print("ID invalid: " + id)
                    print("ID is two letters followed by 4 digits")
                    val = input("Please enter a valid id: ")
                    id = val

            phone = phone[2:len(phone) - 1]                     # removing quotes and making sure phone number is valid
            if check_phone(phone) == False:
                while check_phone(phone) == False:
                    print("Phone " + phone + " is invalid")
                    print("Enter phone number in form 123-456-7890")
                    val = input("Please enter a valid phone number: ")
                    phone = val
            
            new_person = Person(last, first, mi, id, phone)     # creating Person object and adding to dict if id is not repeated
            if id in persons_dict:
                print("there are duplicate IDs in the data")
            persons_dict[id] = new_person

        return persons_dict


def check_id(id):                                               # checks if ID is valid using regex
    regex = re.compile(r'^[a-zA-Z]{2}\d{4}$')
    match = regex.match(id)
    return True if match else False

def check_phone(phone):                                         # checks if phone number is valid using regex
    regex = re.compile(r'^\d{3}-\d{3}-\d{4}$')
    match = regex.match(phone)
    return True if match else False


final_dict = process_file(filepath)

with open('dict.pkl', 'wb') as pickle_file_write:
    pickle.dump(final_dict, pickle_file_write)

with open('dict.pkl', 'rb') as pickle_file_read:
    dict_loaded = pickle.load(pickle_file_read)

for key, value in dict_loaded.items():
    value.display()






