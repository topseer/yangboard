import pyodbc 
import pandas.io.sql as sql

def getEfficiency(user_email):
  #user_email = 'LSOGGE@newdayusa.com'
  server = '10.203.1.105\\alpha' 
  database = 'test_yang' 
  username = 'webuser' 
  password = 'Changeme1' 
  cnxn = pyodbc.connect('DRIVER={ODBC Driver 13 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
  
  query = """

        select Email,PersonID,WaterFallDivision,Team_Desc,FstNm,LstNm,
            
            isnull(SUM(case when MarketingChannel != 'Web' then 1.0*Open_13wk else 0 end) / nullif(SUM(Router_13wk),0),0) as [Router Capture 13wk],
            isnull(SUM(case when MarketingChannel = 'Web' then 1.0*Open_13wk else 0 end) / nullif(SUM(Web_13wk),0),0) as [Web Capture 13wk],
            isnull(SUM(case when MarketingChannel != 'Web' then 1.0*Fund_13wk else 0 end) / nullif(SUM(Router_13wk),0),0) as [Router Close 13wk],
            isnull(SUM(case when MarketingChannel = 'Web' then 1.0*Fund_13wk else 0 end) / nullif(SUM(Web_13wk),0),0) as [Web Close 13wk],
            isnull(SUM(1.0*Pitch_13wk) / nullif(SUM(Open_13wk),0),0) as [Open-Pitch 13wk],
            isnull(SUM(1.0*AO_13wk) / nullif(SUM(Pitch_13wk),0),0) as [Pitch-AO 13wk],

            isnull(SUM(case when MarketingChannel != 'Web' then 1.0*Open_BM else 0 end) / nullif(SUM(Router_BM),0),0) as [Router Capture BM],
            isnull(SUM(case when MarketingChannel = 'Web' then 1.0*Open_BM else 0 end) / nullif(SUM(Web_BM),0),0) as [Web Capture BM],
            isnull(SUM(case when MarketingChannel != 'Web' then 1.0*Fund_BM else 0 end) / nullif(SUM(Router_BM),0),0) as [Router Close BM],
            isnull(SUM(case when MarketingChannel = 'Web' then 1.0*Fund_BM else 0 end) / nullif(SUM(Web_BM),0),0) as [Web Close BM],
            isnull(SUM(1.0*Pitch_BM) / nullif(SUM(Open_BM),0),0) as [Open-Pitch BM],
            isnull(SUM(1.0*AO_BM) / nullif(SUM(Pitch_BM),0) ,0) as [Pitch-AO BM]
        from AE_Performance_Report_individual_13wks
        where Email = 'aaa@aaa.com'
        group by Email,PersonID,WaterFallDivision,Team_Desc,FstNm,LstNm
        order by 1
  """
  query = query.replace('aaa@aaa.com',user_email)  

  queryResult = sql.read_sql(query, cnxn)
  
  list(queryResult)
  
   
  return queryResult 


           