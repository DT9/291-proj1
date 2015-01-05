import datetime

def checkDataType(vN):
    dataType = False
    if(vN == "health_care_no" or vN == "employee_no" or vN == "type_id" or vN == "test_id" or vN == "patient_no" ):
        dataType = "int"
    if(vN == "lab_name"):
        dataType = "varchar(25)"
    if(vN == "test_name"):
        dataType = "varchar(48)"
    if(vN == "name" or vN == "clinic_adress"):
        dataType = "varchar(100)"
    if(vN == "adress"):
        dataType = "varchar(200)"
    if(vN == "pre_requirement" or vN == "test_procedure" or vN == "result"):
        dataType = "varchar(1024)"
    if(vN == "phone" or vN == "office_phone" or vN == "emergency_phone"):
        dataType = "char(10)"
    if(vN == "birth_day" or vN == "prescribe_date" or vN == "test_date"):
        dataType = "date"   
    return dataType

def checkValid(variableName, inputValue):
    if(inputValue == ""):
        print("Empty string.")
        return False
    if((inputValue == "null" or inputValue == "NULL") and (variableName == "name" or variableName == "clinic_address" or variableName == "adress" or variableName == "phone" or variableName == "test_name")):
        print("The " + variableName + " cannot be null")
        return False
    else:
        return True
    dataType = checkDataType(variableName)
    if(dataType == "int"):
        try:
            val = int(inputValue)
            return True
        except ValueError:
            print("Not a positive integer.")
            return False
    if("char" in dataType):
        variableLength = int(''.join(i for i in dataType if i.isdigit()))
        inputLength = len(inputValue)
        if(inputLength <= variableLength):
            return True
        else:
            print("Too many characters. Input must be " + str(variableLength) + " characters at maximum. You inputted " + str(inputLength) + " characters.")
            return False
    if(dataType == "date"):
        if(len(inputValue) != 10):
            print("Not a valid date in the form \"MM/DD/YYYY\".")
            return False
        dateValue = True
        month = inputValue[0] + inputValue[1]
        day = inputValue[3] + inputValue[4]
        year = inputValue[6] + inputValue[7] + inputValue[8] + inputValue[9]
        slash = inputValue[2] + inputValue[5]        
        try:
            newDate = datetime.datetime(int(year),int(month),int(day))
        except ValueError:
            dateValue = False
        if(slash != "//"):
            dateValue = False
        if(dateValue):
            return True
        else:
            print("Not a valid date in the form \"MM/DD/YYYY\".")
            return False    

def inputData(variableName):
    valid = False
    while(True):
        print("Input the " + variableName)
        inputValue = input()
        valid = checkValid(variableName, inputValue)
        if(valid == False):
            continue
        while(True):
            print("Is " + inputValue + " correct? [y/n]")
            response = input()
            if(response == "y" or response == "Y"):
                return inputValue
            elif(response == "n" or response == "N"):
                break
            else:
                print("Please enter y or n")

def collectInputs(variables, variableNames):
    for i in range(0, len(variables)):
        variables[i] = inputData(variableNames[i])
