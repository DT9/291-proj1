import cx_Oracle
from InputCheck import *

def findPrescription(curs, presVariables):
    query = "Select t.test_id From test_record t Where t.type_id = " + presVariables[0] +  " and t.patient_no = " + presVariables[1] + " and t.employee_no = " + presVariables[2] + " and t.prescribe_date = to_date(" + presVariables[3] + ", 'MM/DD/YYYY')"
    #print(query)
    curs.execute(query)
    test_id = curs.fetchall()
    if(test_id):
        test_id = "'" + str(test_id[0][0]) + "'"
        return test_id
    else:
        print("No prescription matches the inputted values.")
        return False

def updateRecord(curs, updateVariables, test_id):
    query1 = "Update test_record set medical_lab = " + updateVariables[0] + " where test_id = " + test_id
    if(updateVariables[1] == "null"):
        query2 = "Update test_record set test_date = " + updateVariables[1] + " where test_id = " + test_id
    else:
        query2 = "Update test_record set test_date = to_date(" + updateVariables[1] + ", 'MM/DD/YYYY') where test_id = " + test_id
    query3 = "Update test_record set result = " + updateVariables[2] + " where test_id = " + test_id
    #print(query1)
    curs.execute(query1)
    #print(query2)
    curs.execute(query2)
    #print(query3)
    curs.execute(query3)
    
def medicalTest(curs):
    test_id = ""
    type_id = ""
    patient_no = ""
    employee_no = ""
    medical_lab = ""
    result = ""
    prescribe_date = ""
    test_date = ""
    presVariables = [type_id, patient_no, employee_no, prescribe_date]
    presVariableNames = ["type_id", "patient_no", "employee_no", "prescribe_date"]
    updateVariables = [medical_lab, test_date, result]
    updateVariableNames = ["medical_lab", "test_date", "result"]
    
    collectInputs(presVariables, presVariableNames)
    test_id = findPrescription(curs, presVariables)
    if(test_id == False):
        print("Invalid Prescription")
        return 0
    else:
        print("Valid Prescription found at test_id: " + test_id + ".")
    
    collectInputs(updateVariables, updateVariableNames)
    curs.execute("Select m.lab_name From medical_lab m Where m.lab_name = " + updateVariables[0])
    labExists = curs.fetchall()
    if(labExists == []):
        print("The medical lab does not exist.")
    else:
        updateRecord(curs, updateVariables, test_id)
        print("Successfully Updated Test Record")
    return 0

#    if(labExists == []):
#	#print('The medical lab does not exist.')
#	pass
#    else:
#	updateRecord(curs, updateVariables, test_id)
#	#print('Successfully Updated Test Record')
#    return 0
