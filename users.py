
from django.contrib.auth.models import User
import pyodbc 
import pandas.io.sql as sql
import pandas as pd

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
"""

queryResult = sql.read_sql(query, cnxn)
 

for i in range(len(queryResult)):
  name = queryResult["UserName"][i]
  pw = queryResult["Password"][i]
  email = queryResult["email"][i]
  print (name, pw, email)
  User.objects.create_user(qname,email, pw)