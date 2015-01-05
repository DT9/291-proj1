from random import randint # has the "randint" function
from SearchEngine import *
#####################################################################################
# Function: prescriptionInfo
# Purpose:  Calls appropriate functions to create a prescription  
#####################################################################################
def prescripInfo(cursor):
   emp = getEmpNum()
   hcn = getPatientInfo(cursor)
   testType = get_test_type(cursor)
   testID = makeTestID(cursor)
   
   cursor.execute("UPDATE test_record set employee_no = " + emp + " patient_no = " + hcn)
   cursor.execute("UPDATE test_record set type_id = " + testType + " patient_no = " + hcn)
   cursor.execute("UPDATE test_record set test_id = " + testID + " patient_no = " + hcn)
    
   
   
   
#####################################################################################
# Function: getEmpNum
# Purpose:  get either employee ID or name of doctor 
# Method:   Prompt if entering name or ID, verifies valid, returns value
# Returns:  Either employee number or their name
#####################################################################################
def getEmpNum():
   valid = False
   
   while (valid == False):
      option = input("Would you like to enter the (n)ame of the doctor or their (e)mployee ID? ")
      if (option == 'n' or option == 'N'):
         fname = input("Please enter their first name: ")
         lname = input("Please enter their last name: ")
         empName = fname+lname
         if not fname.isalpha():
            print("Invalid name")
         else:
            return empName
      elif (option == 'e' or option == 'E'):
         empID = input("Please enter their employee ID: ")
         if not empID.isdigit():
            print("Invalid Employee number")
         else:
            return empID
      else:
         print("Invalid choice.")
         
#####################################################################################
# Function: getPateintInfo
# Purpose:  get either health care number or name of patient from the user 
# Method:   Prompt if entering name or hcn, verifies valid, returns value
# Returns:  either hcn or patient name
#####################################################################################          
def getPatientInfo(cursor):
   valid = False
   
   while (valid == False):
      option = input("Would you like to enter the (n)ame of the patient or their (h)ealth care number? ")
      if (option == 'n' or option == 'N'):
         fname = input("Please enter their first name: ")
         lname = input("Please enter their last name: ")
         patientName = fname+lname
         
         if not patientName.isalpha():
            print("Invalid name")
         else:
            patient_info(cursor,patientName)
            return patientName
      elif (option == 'h' or option == 'H'):
         hcn = input("Please enter their health care number: ")
         if not hcn.isdigit():
            print("Invalid health care number")
         else:
            patient_info(cursor,hcn)
            return hcn
      else:
         print("Invalid choice.")        
         
#####################################################################################
# Function: get_test_type
# Purpose:  To take input from user about what test is being prescribed
# Method:   Ask user for name of test, verify correct, check it doesnt conflict with
#           any of the tests patient is not allowed to take
# Returns:  testname
#####################################################################################
def get_test_type(cursor):
   valid = False
   
   while (valid == False):
      testName = input("Please enter the test number: ")
      # verify correct name
      yesno = input("Please verify that |" + testName + "| is the correct test (Y/N): ")
      if (yesno == 'y' or yesno == 'Y'):
         #call testConflict here. if valid then return testName
         conflict = testConflict(cursor,testName)
         if (conflict == False):
            return testName
   
  
    
#####################################################################################
# Function: makeTestID
# Purpose:  Creates a test ID number 
# Method:   Uses randint to create a random number between 1000 and 1999
# Returns:  testID
#####################################################################################    
def makeTestID(cursor):
   valid = False
   while (valid == False):
      testID = randint(1000, 1999) #check how wide testID nums can be
      cursor.execute("select * from test_record where test_id = '"+str(testID)+"'")
      if not cursor.fetchall():
         valid = True
         
   return testID
      
      
#####################################################################################
# Function:   testConflict
# Parameters: typeID: type of test patient will take
# Purpose:    Check if patient is not allowed to take the test prescriped 
# Method:     Checks doctor entered test type against patients not allowed types
# Returns:    True if theres a conflict, false otherwise
#####################################################################################
def testConflict(cursor,typeID):
   cursor.execute("select * from not_allowed where test_id = '"+typeID+"'")
   if cursor.fetchall():
      return True
   return False
 

        
            
        
