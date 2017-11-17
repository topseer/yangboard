import pyodbc 
import pandas.io.sql as sql

def get_LeadsVolume():
  #user_email = 'btaylor@newdayusa.com'
  server = '10.203.1.105\\alpha' 
  database = 'test_yang' 
  username = 'webuser' 
  password = 'Changeme1' 
  cnxn = pyodbc.connect('DRIVER={ODBC Driver 13 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
  
  query = """  
    select * from LeadsVolumeByTimeoftheDay
  """

  queryResult = sql.read_sql(query, cnxn)
    
  return queryResult 

if __name__ == "__main__":
  user_email = 'yxu@newdayusa.com'
  queryResult = get_LeadsVolume ()
  
   
  
 