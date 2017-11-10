import pyodbc 
import pandas.io.sql as sql

def get_AEPipeline(user_email):
  #user_email = 'btaylor@newdayusa.com'
  server = '10.203.1.105\\alpha' 
  database = 'test_yang' 
  username = 'webuser' 
  password = 'Changeme1' 
  cnxn = pyodbc.connect('DRIVER={ODBC Driver 13 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
  
  query = """  

    select LoanNum,BorrName, LstStsDtCdDesc, convert(varchar, CurrentStsDate,110) CurrentStsDate,
		   isnull(isnull(BorrPh,BorrMobilePh),' ') as BorrPh , 
		   isnull(convert(varchar,LastCallTime,120),'NA') as LastCallTime
    from DashboardReport_LoanStatus_1
    where AE_Email = 'aaa@aaa.com'
  """
  query = query.replace('aaa@aaa.com',user_email)  

  queryResult = sql.read_sql(query, cnxn)

  return queryResult.as_matrix().tolist()
  
 