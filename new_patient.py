import cx_Oracle
from SearchEngine import *
from InputCheck import *

#####################################################################################
# Function: choices
# Purpose:  Depending on if user wants to create/edit patient, calls appropriate 
#           function
# Method:   Prompts for verification on create/edit
#####################################################################################
def choices(cursor,choice):
    valid = False 
   
    if choice == 'c' or choice == 'C':
        while (valid == False):                                               # verify person wants to add new patient
            option = input("Please verify you would like to create a new patient (Y/N): ")
            if option == 'N' or option == 'n':
                return                                                         # they dont, go back to caller
            elif option == 'Y' or option == 'y':
                valid = True        
            new_patient(cursor)
    else:
        while (valid == False):                                               # verify person wants to add new patient
            option = input("Please verify you would like to edit a patient (Y/N): ")
            if option == 'N' or option == 'n':
                return                                                         # they dont, go back to caller
            elif option == 'Y' or option == 'y':
                         
                edit_patient(cursor)
            else:
                valid = False
            
  
#####################################################################################
# Function: new_patient
# Purpose:  Call functions needed to create a new patient 
#           Inserts new patient into database            
#####################################################################################       
def new_patient(cursor):
    
#    name = str(change_name())
#    hcn = str(new_hcn())
#    addr = str(change_addr())
#    bday = str(change_bday())
#    phoneNum = str(change_phoneNum())
#    cantTake = str(test_cant_take())
    name = ""
    health_care_no = ""
    address = ""
    birth_day = ""
    phone = ""
    patientVariables = [name, health_care_no, address, birth_day, phone]
    patientVariableNames = ["name", "health_care_no", "address", "birth_day", "phone"]
    collectInputs(patientVariables, patientVariableNames)
    print(collectInputs)  
   
 #   cursor.execute("insert into patient values (:hcn, :name, :addr, to_date(:bday,'mm/dd/yyyy'), :phone)",{'hcn':hcn,'name':name,'addr':addr,'bday':bday,'phone':phoneNum})
 #   if (cantTake != False):
 #       cursor.execute("insert into not_allowed values (:hcn, :type_id)",{'hcn':hcn, 'type_id':cantTake})


#####################################################################################
# Function: test_cant_take
# Purpose:  Collect information on tests patient cant take 
# Method:   Prompt if there are any test cant take, verifies correct
# Returns:  test patient cant take
#####################################################################################
def test_cant_take():
    valid = False
    
    while (valid == False):
        yesno = input("Are there any tests which the patient can not have (Y/N)? ")
        if (yesno == 'Y' or yesno =='y'):
            cantTake = input("Enter the ID of the test the patient is unable to take: ")
            yesno = input("Please verify that the test: |" + cantTake + "| is the one which patient can not take (Y/N): ")
          
            if (yesno == 'y' or yesno == 'Y'):
                return cantTake
        elif (yesno == 'N' or yesno == 'n'):
            return False
        else:
            print("Invalid choice ")
        
        
            
#####################################################################################
# Function: change_phoneNum
# Purpose:  To get a patients phone number 
# Method:   Prompt for phone number, verify its a digit
# Returns:  Phone number
#####################################################################################        
def change_phoneNum():
    valid = False
    
    while (valid == False):
        phoneNum = input("Please enter the new phone number. Please do not enter any dashes (-) or brackets: ")
        if not phoneNum.isdigit():
            print("Invalid formatting")
            
        elif len(phoneNum) > 10:                                               # phone num must be at most 10 digits
            print("Inavlid number. Should not have more than ten (10) numbers")
            
        else:
            yesno = input("Please verify |" + phoneNum +"| as he new phone number (Y/N): ")
            if (yesno == 'y' or yesno =='Y'):  
                return phoneNum
   
#####################################################################################
# Function: change_bday
# Purpose:  To edit or create the birthdate of a patient
# Method:   Prompt for info, verify correct
# Returns:  birthday
#####################################################################################   
def change_bday():
    valid = False
    
    while (valid == False):
        bday = input("Please enter the new birthday in the format of mm/dd/yyyy: ")
        yesno = input("Please verify the following as the correct birthday |" + bday + "| (Y/N): ")
        if (yesno == 'Y' or yesno == 'y'):
            
            valid = True
    return bday
            
#####################################################################################
# Function: change_addr
# Purpose:  Change patients address
# Method:   Prompt for addr, verify correct
# Returns:  addr
#####################################################################################   
def change_addr():
    valid = 'N'
        
    while (valid == 'N'):
        addr = input("Please enter the new address:  ")
        valid = input("Please verify that |" + addr + "| is the correct address (Y/N): ")
        if (valid == 'Y' or valid == 'y'):
            return addr            
            
        else:
            if (valid != 'N' or valid != 'n'):
                print("Invalid option.")
            valid = 'N'
            
#####################################################################################
# Function: new_hcn
# Purpose:  Create a new health care number
# Method:   Prompts for the hcn, verify correct
# Returns:  hcn
#####################################################################################         
def new_hcn():
    valid = False
    
    while (valid == False):
        hcn = input("Please enter the new Health Care Number: ")
        if not hcn.isdigit():
            print("Invalid Health Care Number. Please ensure you are entering a number.")
        else: 
            yesno = input("Please verify |" +hcn+"| as the new health care number (Y/N): ")    
            if (yesno == 'y' or yesno == 'Y'):
                print("The new Health Care Number is |" + hcn + "|")
                return hcn
   

#####################################################################################
# Function: change_name
# Purpose:  Create/change name of a patient
# Method:   Prompt user for patient name, verify correct
# Returns:  name
#####################################################################################      
def change_name():    
    valid = False    
    # assume no middle name
    valid = False                                                               # prep for new loop
    while (valid == False):
        fname = input("Please enter the patient's new first name: ")            # first name
        if not fname.isalpha():                                                # verify name is a string
            print("Invalid name.")
            
        else:                                                                   # will enter if fname is valid
            lname = input("Please enter their last name: ")
            if not lname.isalpha():                                            # if last name is not string, invalid
                print("Invalid name")
            else:
                valid = True;                                                   # else first and last name are valid input, can exit loop
    
    fullName = fname + " " + lname
    print("The patient's name is |" + fullName + "|")
    return fullName
        

#####################################################################################
# Function: edit_patient
# Purpose:  Calls appropriate functions to edit a patient
# Method:   Prompts user what they would like to do; does it
#           Updates appropriate patient in database
#####################################################################################   
def edit_patient(cursor):
    valid = False
    hcn = find_HCN()
    
    while (valid == False):
        print("What would you like to do?")
        choice = input("Change (n)ame, change (a)ddress, change (b)irthday, change (p)hone number, change (t)ests patient cant take, (q)uit: ")
        
        if (choice == 'n' or choice == 'N'):
            name = change_name()
            valid = True
            cursor.execute("UPDATE patient set name = '" + name + "' where health_care_no = " + hcn)
            
        elif (choice == 'a' or choice == 'A'):
            addr = change_addr()
            valid = True
            cursor.execute("UPDATE patient set address= '" + addr + "' where health_care_no = " + hcn)
            
        elif (choice == 'b' or choice == 'B'):
            bday = change_bday()
            valid = True
            cursor.execute("UPDATE patient set birth_day = to_date('" + bday + "','MM/DD/YYYY') where health_care_no = " + hcn)
            
        elif (choice == 'p' or choice == 'P'):
            phoneNum = change_phoneNum()
            valid = True
            cursor.execute("UPDATE patient set phone = " + phoneNum + " where health_care_no = " + hcn)
            
        elif (choice =='t' or choice == 'T'):
            cantTake = test_cant_take()
            vaild = True            
            cursor.execute("UPDATE not_allowed set test_id = " + cantTake + " where health_care_no = " + hcn)
            
        elif (choice == 'q' or choice == 'Q'):
            valid = True
            return 
            
        else:
            print("Invalid input.")

            
#####################################################################################
# Function: find_HCN
# Purpose:  Collect patients health care number
# Method:   Prompt, verify
#####################################################################################                         
def find_HCN():
    valid = False

    while (valid == False):
        hcn = input("Enter the patient's health care number: ")
        yesno = input ("Please verify that |" + hcn + "| is the correct health care number (y/n): ")
        if (yesno == 'y' or yesno == 'Y'):
            valid = True
    return hcn           


