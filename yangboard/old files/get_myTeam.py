import pyodbc 
import pandas.io.sql as sql

def get_myTeam(user_email):
  #user_email = 'btaylor@newdayusa.com'
  server = '10.203.1.105\\alpha' 
  database = 'test_yang' 
  username = 'webuser' 
  password = 'Changeme1' 
  cnxn = pyodbc.connect('DRIVER={ODBC Driver 13 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
  
  query = """  
    select case when left(FstNm,charindex(' ',fstnm,1)) ='' then FstNm else left(FstNm,charindex(' ',fstnm,1)) end +' '+ LstNm as Name,
		   email as Email
    from topDownAELookupTable
    where Team_Desc = (select Team_Desc from topDownAELookupTable where Email = 'aaa@aaa.com')
  """
  query = query.replace('aaa@aaa.com',user_email)  

  queryResult = sql.read_sql(query, cnxn)

  return queryResult.as_matrix().tolist()





 
 