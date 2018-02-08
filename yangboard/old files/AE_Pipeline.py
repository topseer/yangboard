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
    select LoanNum,
		   Score = case when Conv_Score_Group2 in ('Fair','Warm') then 'A' when Conv_Score_Group2 in ('Hot','On Fire') then 'AA' else 'AAA' end , 
		   BorrName, LstStsDtCdDesc, convert(varchar, CurrentStsDate,110) CurrentStsDate, 
		   datediff(DAY,CurrentStsDate,getdate()) as DaysInCurrentStatus,
		   isnull(isnull(BorrPh,BorrMobilePh),' ') as BorrPh , 
		   isnull(convert(varchar,LastCallTime,120),'NA') as LastCallTime,
		   datediff(day,LastCallTime,getdate()) as DaysSinceLastContact 
    from DashboardReport_LoanStatus_1
    where AE_Email = 'aaa@aaa.com'
  """
  query = query.replace('aaa@aaa.com',user_email)  

  queryResult = sql.read_sql(query, cnxn)

  return queryResult.as_matrix().tolist()
  
 