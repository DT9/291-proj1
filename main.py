import cx_Oracle
from prescription import *
from new_patient import *
from MedicalTest import *
from SearchEngine  import *

#global variables 
conString = ''
connection =''
cursor=''

def main():

	global conString
	global connection
	global cursor
	#prompt for user and pw
	#user = input("Username: ")
	#pw = input("Password: ")
	user = 'dtruong1'
	pw = 'hunter23'
	#create connection
	conString= user+'/' + pw +'@gwynne.cs.ualberta.ca:1521/CRS'
	connection = cx_Oracle.connect(conString)
	cursor = connection.cursor()

	#prompt for program
	valid = False
	while (valid == False):
		choice = input("Would you like to (s)earch for a patient, create a (p)rescription, enter (m)edical test results, (u)pdate/(c)reate a patient, or (q)uit?: ")
		if (choice == 's' or choice == 'S'):
			Search(cursor)
			valid = True
			connection.commit()
		elif (choice == 'p' or choice == 'P'):
			prescripInfo(cursor)
			valid = True
			connection.commit()
		elif (choice == 'm' or choice == 'M'):
			medicalTest(cursor) # verify with austin what his main fun is
			valid = True
			connection.commit()
		elif (choice == 'u' or choice == 'U' or choice == 'c' or choice == 'C'):
			choices(cursor,choice)
			connection.commit()
		elif (choice == 'q' or choice == 'Q'):
			break
		else:
			print("Invalid option")
	
		    
	connection.commit()
	cursor.close()
	connection.close()
main()
