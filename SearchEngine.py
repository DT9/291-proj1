import cx_Oracle
user = "dtruong1"
pw = "hunter23"


def Search(cursor):
  while (True):
    string = input("Choose a program: Patient info (1), Doctor prescriptions (2), Alarming age (3): ")
    if string in "123":
      break
    print("Invalid input, try again")
    
  if string == "1":
    pid_name = input("Enter patient id or name: ")
    patient_info(cursor,pid_name)
  elif string == '2':
    while True:
      doctor = input("Enter doctor employee id or name, start and end dates as follows: (John Doe,12/12/2000,11/11/1999): ").split(',')
      if len(doctor) == 3:
        break
      print("Invalid input")
    test_record(cursor,doctor[0],doctor[1],doctor[2])
  elif string == '3':
    alarm = input("Enter a test type name: ")
    alarming_age(cursor,alarm)
      
def patient_info(cursor,name_id):
  #name_id = input("Please input the patient's name or healthcare id: " )
  if name_id.isdigit(): #if healthcare no. assign string to hcid
    string = "r.patient_no = "+name_id
  else:
    string = "p.name = '"+name_id+"'"  #otherwise assign to name
  
  query = "select p.health_care_no, p.name, t.test_name, to_char(r.test_date,'MM/DD/YYYY'),r.result from patient p, test_record r, test_type t where "+string+" and r.type_id = t.type_id and p.health_care_no = r.patient_no"
  cursor.execute(query)
  rows = cursor.fetchall()
  
  for row in rows:
    print(row)
  
def test_record(cursor,doctor_id_name,start_date,end_date):
  
  #doctor_id_name = input("Please input the doctor's name or employee id: ")
  #start_date = input("Please input the start date in MM/DD/YYYY format: ")
  #end_date = input("Please input the end date in MM/DD/YYYY format: ")

  if doctor_id_name.isdigit():
    string = "d.employee_no = "+ doctor_id_name
  else:
    string = "p.name = '"+doctor_id_name+"'"
  
  query = "select p.health_care_no, p.name,t.test_name,r.prescribe_date from test_record r, patient p,doctor d, test_type t where "+string+" and t.type_id = r.type_id and p.health_care_no = r.patient_no and d.health_care_no = p.health_care_no and r.prescribe_date between to_date('"+start_date+"','MM/DD/YYYY') and to_date('"+end_date+"','MM/DD/YYYY')"
  cursor.execute(query)
  rows = cursor.fetchall()
  
  for row in rows:
    print(row)
  
def alarming_age(cursor,test_type):
  try:
    #test_type = input("Please input the test name: ")
    while test_type.isdigit():
      print("Invalid input")
      test_type = input("Please input the test name: ")
    drop = "DROP VIEW medical_risk"
    query = "CREATE VIEW medical_risk(medical_type,alarming_age,abnormal_rate) AS SELECT c1.type_id,min(c1.age),ab_rate FROM  (SELECT   t1.type_id, count(distinct t1.patient_no)/count(distinct t2.patient_no) ab_rate     FROM     test_record t1, test_record t2      WHERE    t1.result <> 'normal' AND t1.type_id = t2.type_id      GROUP BY t1.type_id      ) r,     (SELECT   t1.type_id,age,COUNT(distinct p1.health_care_no) AS ab_cnt      FROM     patient p1,test_record t1,               (SELECT DISTINCT trunc(months_between(sysdate,p1.birth_day)/12) AS age FROM patient p1)       WHERE    trunc(months_between(sysdate,p1.birth_day)/12)>=age               AND p1.health_care_no=t1.patient_no               AND t1.result<>'normal'      GROUP BY age,t1.type_id      ) c1,  	      (SELECT  t1.type_id,age,COUNT(distinct p1.health_care_no) AS cnt       FROM    patient p1, test_record t1,      	       (SELECT DISTINCT trunc(months_between(sysdate,p1.birth_day)/12) AS age FROM patient p1)       WHERE trunc(months_between(sysdate,p1.birth_day)/12)>=age             AND p1.health_care_no=t1.patient_no       GROUP BY age,t1.type_id      ) c2 WHERE  c1.age = c2.age AND c1.type_id = c2.type_id AND c1.type_id = r.type_id        AND c1.ab_cnt/c2.cnt>=2*r.ab_rate GROUP BY c1.type_id,ab_rate"
    age = "SELECT DISTINCT name, address, phone FROM   patient p, medical_risk m WHERE  trunc(months_between(sysdate,birth_day)/12) >= m.alarming_age AND       p.health_care_no NOT IN (SELECT patient_no                                FROM   test_record t, test_type type                                WHERE  m.medical_type = t.type_id                                AND    t.type_id = type.type_id                                AND    type.test_name = '"+test_type+"'                               )"
    cursor.execute(drop)
    cursor.execute(query)
    cursor.execute(age)
    rows = cursor.fetchall()
    
    for row in rows:
      print(row)
  
  except cx_Oracle.DatabaseError as exc:
    error, = exc.args
    print( sys.stderr, "Oracle code:", error.code)
    print( sys.stderr, "Oracle message:", error.message)
  
