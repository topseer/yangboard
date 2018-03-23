import pyodbc 
import pandas.io.sql as sql

def get_AEPipeline(user_email,isPrch):
  #user_email = 'btaylor@newdayusa.com'
	query = """ 
	  select LoanNum,
		   Score = case when Conv_Score_Group2 in ('Fair','Warm') then 'A' when Conv_Score_Group2 in ('Hot','On Fire') then 'AA' else 'AAA' end , 
		   BorrName, LstStsDtCdDesc, convert(varchar, CurrentStsDate,110) CurrentStsDate, 
		   datediff(DAY,CurrentStsDate,getdate()) as DaysInCurrentStatus,
		   isnull(isnull(BorrPh,BorrMobilePh),' ') as BorrPh , 
		   isnull(convert(varchar,LastCallTime,120),'NA') as LastCallTime,
		   isnull(datediff(day,LastCallTime,getdate()),'14') as DaysSinceLastContact ,
		   Comments 
    from DashboardReport_LoanStatus_1  
    where AE_Email = 'aaa@aaa.com' """	

	server = '10.203.1.105\\alpha' 
	database = 'test_yang' 
	username = 'webuser' 
	password = "Changeme1"
	cnxn = pyodbc.connect('DRIVER={ODBC Driver 13 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)	
	
	if (isPrch): 
	  query = """  
     	select LoanNum,HmSt, 
		   BorrName,
			 CoBorrName, 
			 LstStsDtCdDesc, 
		   convert(varchar, CurrentStsDate,110) CurrentStsDate, 
		   --datediff(DAY,CurrentStsDate,getdate()) as DaysInCurrentStatus,
		   isnull(isnull(BorrPh,BorrMobilePh),' ') as BorrPh , 
		   left(isnull(convert(varchar,LastCallTime,120),'NA'),10) as LastCallTime,
		   --isnull(datediff(day,LastCallTime,getdate()),'14') as DaysSinceLastContact ,
		   isnull(left(convert(varchar,NextExpirationDate,110),10),'NA') NextExpirationDate,
		   NextExpirationDate_Name,		   
		   isnull(left(convert(varchar,ContractExpirationDate,110),10),'NA') ContractExpirationDate,
		   Comments   
    	from DashboardReport_LoanStatus_1  
    	where AE_Email = 'aaa@aaa.com'
	"""		
  
	query = query.replace('aaa@aaa.com',user_email)  
	queryResult = sql.read_sql(query, cnxn)
	queryResult_PreQual = queryResult.drop(queryResult.index)
	queryResult_PreQual = queryResult.loc[queryResult["LstStsDtCdDesc"].isin(["PRE QUAL ISSUED","PRE APPROVED"])]
	queryResult = queryResult.loc[~queryResult["LstStsDtCdDesc"].isin(["PRE QUAL ISSUED","PRE APPROVED"])]

	return queryResult.as_matrix().tolist(),queryResult_PreQual.as_matrix().tolist()
  
def get_TeamPipeline(user_email,isPrch):
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
		   isnull(datediff(day,LastCallTime,getdate()),'14') as DaysSinceLastContact ,
		   Comments,AE_Email,AE_PersonID
    from DashboardReport_LoanStatus_1  as a 
	  where a.AE_PersonID in (
 
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
     	select LoanNum,HmSt, 
		   BorrName,
			 AccountExec, 
			 LstStsDtCdDesc, 
		   convert(varchar, CurrentStsDate,110) CurrentStsDate, 
		   --datediff(DAY,CurrentStsDate,getdate()) as DaysInCurrentStatus,
		   isnull(isnull(BorrPh,BorrMobilePh),' ') as BorrPh , 
		   left(isnull(convert(varchar,LastCallTime,120),'NA'),10) as LastCallTime,
		   --isnull(datediff(day,LastCallTime,getdate()),'14') as DaysSinceLastContact ,
		   isnull(left(convert(varchar,NextExpirationDate,110),10),'NA') NextExpirationDate,
		   NextExpirationDate_Name,		   
		   isnull(left(convert(varchar,ContractExpirationDate,110),10),'NA') ContractExpirationDate,
		   Comments   
    from DashboardReport_LoanStatus_1  as a 
	  where a.AE_PersonID in (
 
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
  queryResult_PreQual = queryResult.drop(queryResult.index)
  queryResult_PreQual = queryResult.loc[queryResult["LstStsDtCdDesc"].isin(["PRE QUAL ISSUED","PRE APPROVED"])]
  queryResult = queryResult.loc[~queryResult["LstStsDtCdDesc"].isin(["PRE QUAL ISSUED","PRE APPROVED"])]
	
  return queryResult.as_matrix().tolist(),queryResult_PreQual.as_matrix().tolist()
  
  