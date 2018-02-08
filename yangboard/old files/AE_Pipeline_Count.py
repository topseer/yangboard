import pyodbc 
import pandas.io.sql as sql

def get_AEPipeline_Count(user_email):
  #user_email = 'btaylor@newdayusa.com'
  server = '10.203.1.105\\alpha' 
  database = 'test_yang' 
  username = 'webuser' 
  password = 'Changeme1' 
  cnxn = pyodbc.connect('DRIVER={ODBC Driver 13 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
  
  query = """  
        with Abcd as (  
        select a.personid, b.Email,
            sum(case when PreInProcessDtm is not null and ApprOrdDate is not null and InProcessDate is null then 1 else 0 end) as Pip,
            sum(case when PreInProcessDtm is not null and ApprOrdDate is not null and InProcessDate is null then LoanAmt else 0 end) as Pip_LoanAMT,
            sum(case when InProcessDate is not null then 1 else 0 end) as IP,
            sum(case when InProcessDate is not null then LoanAmt else 0 end) as IP_LoanAmt	   
        from AEMatrix_Report_CurrentPipe as a 
        inner join topDownAELookupTable as b 
        on a.PersonID = b.PersonId
        group by a.personid,b.Email
        )
        select a.Email,a.Pip,a.IP,count(*) as TotalPipe 
        from Abcd as a 
        inner join DashboardReport_LoanStatus_1 as b 
        on a.PersonID = b.AE_PersonID
        where b.AE_Email = 'aaa@aaa.com'
        group by a.Email,a.Pip,a.IP
  """
  query = query.replace('aaa@aaa.com',user_email)  

  queryResult = sql.read_sql(query, cnxn)

  return queryResult
 