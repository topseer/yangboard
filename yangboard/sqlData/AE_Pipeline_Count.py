import pyodbc 
import pandas.io.sql as sql

def get_AEPipeline_Count(user_email,isPrch):
  #user_email = 'btaylor@newdayusa.com'
  server = '10.203.1.105\\alpha' 
  database = 'test_yang' 
  username = 'webuser' 
  password = 'Changeme1' 
  cnxn = pyodbc.connect('DRIVER={ODBC Driver 13 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
  
  query = """  
        with Abcd as (  
        select a.AE_PersonID as PersonID, b.Email,
            sum(case when PreInProcessDtm is not null and ApprOrdDate is not null and InProcessDate is null then 1 else 0 end) as Pip,
            sum(case when PreInProcessDtm is not null and ApprOrdDate is not null and InProcessDate is null then LoanAmt else 0 end) as Pip_LoanAMT,
            sum(case when InProcessDate is not null then 1 else 0 end) as IP,
            sum(case when InProcessDate is not null then LoanAmt else 0 end) as IP_LoanAmt	   ,   
			      count(*) as TotalLoans
        from DashboardReport_LoanStatus_1 as a 
        inner join topDownAELookupTable as b 
        on a.AE_PersonID = b.PersonId
        group by a.AE_PersonID,b.Email
        )
        select a.Email,a.Pip,a.IP,count(*) as TotalPipe 
        from Abcd as a 
        inner join DashboardReport_LoanStatus_1 as b 
        on a.PersonID = b.AE_PersonID
        where b.AE_Email = 'aaa@aaa.com'
        group by a.Email,a.Pip,a.IP
  """

  if (isPrch): 
	  query = """  
        with Abcd as (  
        select a.AE_PersonID as PersonID, b.Email,
            sum(case when ApplicationDtm is not null then 1 else 0 end) as Pip,
            sum(case when PreInProcessDtm is not null and ApprOrdDate is not null and InProcessDate is null then LoanAmt else 0 end) as Pip_LoanAMT,            
			      count(*) - sum(case when ApplicationDtm is not null then 1 else 0 end) as IP,
            sum(case when InProcessDate is not null then LoanAmt else 0 end) as IP_LoanAmt	   ,   
			      count(*) as TotalLoans
        from DashboardReport_LoanStatus_1 as a 
        inner join topDownAELookupTable as b 
        on a.AE_PersonID = b.PersonId
        group by a.AE_PersonID,b.Email
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



def get_TeamPipeline_Count(user_email,isPrch):
  #user_email = 'btaylor@newdayusa.com'
  server = '10.203.1.105\\alpha' 
  database = 'test_yang' 
  username = 'webuser' 
  password = 'Changeme1' 
  cnxn = pyodbc.connect('DRIVER={ODBC Driver 13 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
  
  query = """  
        with Abcd as (  
        select a.AE_PersonID as PersonID, b.Email,
            sum(case when PreInProcessDtm is not null and ApprOrdDate is not null and InProcessDate is null then 1 else 0 end) as Pip,
            sum(case when PreInProcessDtm is not null and ApprOrdDate is not null and InProcessDate is null then LoanAmt else 0 end) as Pip_LoanAMT,
            sum(case when InProcessDate is not null then 1 else 0 end) as IP,
            sum(case when InProcessDate is not null then LoanAmt else 0 end) as IP_LoanAmt	   ,   
			  count(*) as TotalLoans
        from DashboardReport_LoanStatus_1 as a 
        inner join topDownAELookupTable as b 
        on a.AE_PersonID = b.PersonId
        group by a.AE_PersonID,b.Email
        )
        select 'aaa@aaa.com' as AE_Email ,sum(a.Pip) as Pip,sum(a.IP) as IP, sum(TotalLoans)  as TotalPipe 
        from Abcd as a         
        where a.PersonID  in (
 
		  select personid
		  from topDownAELookupTable
		  where Team_Desc = (select Team_Desc from topDownAELookupTable where Email = 'aaa@aaa.com')
		  and (
			  (	    (select Employee_Code from topDownAELookupTable where Email = 'aaa@aaa.com') in ('A0PZ','A1HD','A1OO','A0MG','A1NW','A1O7','A1AP','A1O2')
				and Employee_Code  in ('A0PZ','A1HD','A1OO','A0MG','A1NW','A1O7','A1AP','A1O2')
			  ) or

			  (	    (select Employee_Code from topDownAELookupTable where Email = 'aaa@aaa.com') in ('A0Y0','A0KI','A1LC','A1JQ','A1Q3','A1ON','A1K8')
				and Employee_Code  in ('A0Y0','A0KI','A1LC','A1JQ','A1Q3','A1ON','A1K8')
			  ) or

			  (	    (select Employee_Code from topDownAELookupTable where Email = 'aaa@aaa.com') in ('A03H','A12M','A1HT','A1NM','A1FA','A1F7','A1JO','A1Q1','A1IJ')
				and Employee_Code  in ('A03H','A12M','A1HT','A1NM','A1FA','A1F7','A1JO','A1Q1','A1IJ')
			  ) or

			  (	    (select Employee_Code from topDownAELookupTable where Email = 'aaa@aaa.com') in ('A0TC')
				and Employee_Code  in ( select Employee_Code from topDownAELookupTable where Division_Desc = 'Purchase')
			  )
          
			  or Division_Desc != 'Purchase'          
			  )
		    )
  """
  if (isPrch): 
	  query = """  
        with Abcd as (  
        select a.AE_PersonID as PersonID, b.Email,
            sum(case when ApplicationDtm is not null then 1 else 0 end) as Pip,
            sum(case when PreInProcessDtm is not null and ApprOrdDate is not null and InProcessDate is null then LoanAmt else 0 end) as Pip_LoanAMT,            
			      count(*) - sum(case when ApplicationDtm is not null then 1 else 0 end) as IP,
            sum(case when InProcessDate is not null then LoanAmt else 0 end) as IP_LoanAmt	   ,   
			      count(*) as TotalLoans
        from DashboardReport_LoanStatus_1 as a 
        inner join topDownAELookupTable as b 
        on a.AE_PersonID = b.PersonId
        group by a.AE_PersonID,b.Email
        )
        select 'aaa@aaa.com' as AE_Email ,sum(a.Pip) as Pip,sum(a.IP) as IP, sum(TotalLoans)  as TotalPipe 
        from Abcd as a         
        where a.PersonID  in (
 
		  select personid
		  from topDownAELookupTable
		  where Team_Desc = (select Team_Desc from topDownAELookupTable where Email = 'aaa@aaa.com')
		  and (
			  (	    (select Employee_Code from topDownAELookupTable where Email = 'aaa@aaa.com') in ('A0PZ','A1HD','A1OO','A0MG','A1NW','A1O7','A1AP','A1O2')
				and Employee_Code  in ('A0PZ','A1HD','A1OO','A0MG','A1NW','A1O7','A1AP','A1O2')
			  ) or

			  (	    (select Employee_Code from topDownAELookupTable where Email = 'aaa@aaa.com') in ('A0Y0','A0KI','A1LC','A1JQ','A1Q3','A1ON','A1K8')
				and Employee_Code  in ('A0Y0','A0KI','A1LC','A1JQ','A1Q3','A1ON','A1K8')
			  ) or

			  (	    (select Employee_Code from topDownAELookupTable where Email = 'aaa@aaa.com') in ('A03H','A12M','A1HT','A1NM','A1FA','A1F7','A1JO','A1Q1','A1IJ')
				and Employee_Code  in ('A03H','A12M','A1HT','A1NM','A1FA','A1F7','A1JO','A1Q1','A1IJ')
			  ) or

			  (	    (select Employee_Code from topDownAELookupTable where Email = 'aaa@aaa.com') in ('A0TC')
				and Employee_Code  in ( select Employee_Code from topDownAELookupTable where Division_Desc = 'Purchase')
			  )
          
			  or Division_Desc != 'Purchase'          
			  )
		    )
	"""	  
  query = query.replace('aaa@aaa.com',user_email)  

  queryResult = sql.read_sql(query, cnxn)

  return queryResult
  