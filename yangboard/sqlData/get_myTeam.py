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
        email as Email,Employee_Code
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
  """
  query = query.replace('aaa@aaa.com',user_email)  

  queryResult = sql.read_sql(query, cnxn)

  return queryResult.as_matrix().tolist()





 
 