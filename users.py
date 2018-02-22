
from django.contrib.auth.models import User
import pyodbc 
import pandas.io.sql as sql
import pandas as pd
from django.contrib.auth.models import Group


#for i in range(100):

server = '10.203.1.105\\alpha' 
database = 'test_yang' 
username = 'webuser' 
password = 'Changeme1' 
cnxn = pyodbc.connect('DRIVER={ODBC Driver 13 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)

query = """  
select lower(email) email, 
	   lower( left(email, charindex('@',email,1)-1)) as UserName,
	   lower( left(email, charindex('@',email,1)-1)) as Password,
	   WaterFallDivision	   
from topDownAELookupTable
where WaterFallDivision!=''
and ActiveCd = 'Y'
and Email!=''
"""


queryResult = sql.read_sql(query, cnxn)
 

for i in range(len(queryResult)):
  qname = queryResult["UserName"][i]
  pw = queryResult["Password"][i]
  email = queryResult["email"][i]
  waterfalldivision = queryResult["WaterFallDivision"][i]
  user_group = Group.objects.get(name=waterfalldivision)   
  print (qname, pw, email)
  User.objects.create_user(qname,email, pw)
  uid = User.objects.get(username=qname)
  user_group.user_set.add(uid)