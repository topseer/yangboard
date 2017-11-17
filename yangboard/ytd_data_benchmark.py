import pyodbc 
import pandas.io.sql as sql
import pandas as pd

def get_ytdData_bm(user_email):
  #user_email = 'btaylor@newdayusa.com'
  server = '10.203.1.105\\alpha' 
  database = 'test_yang' 
  username = 'webuser' 
  password = 'Changeme1' 
  cnxn = pyodbc.connect('DRIVER={ODBC Driver 13 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
  
  query = """              
          
    select personid, a.WaterFallDivision, 
    	max(a.DivStartDtm) as DivStartDtm,
    	max(a.HireDate) as HireDate,
    	max(a.Tenure) as Tenure,
    	max(a.DivisionTenure) as DivisionTenure,
    	max(a.LiscensedStates) as LS,
    	max(a.Current_IP) Current_IP,
    	max(a.Current_IP_AMT) Current_IP_AMT,
    	max(a.Current_PIP) Current_PIP,
    	max(a.Current_PIP_AMT) Current_PIP_AMT,
    
    	sum(a.IP) as IP,
    	sum(a.LoanAMount_IP) as LoanAMount_IP_Total,
    	avg(a.LoanAMount_IP) as LoanAMount_IP_AVG,
    
    	sum(a.[CO Close]) as [CO Close],
    	sum(a.LoanAMount_CO) as LoanAMount_CO_Total,
    	avg(a.LoanAMount_CO) as LoanAMount_CO_AVG,
    
    	sum(a.AO) as AO,
    	sum(a.LoanAMount_AO) as LoanAMount_AO,
    
    	sum(a.CurrQTR_CO_AMT) as CurrQTR_CO_AMT,
    	sum(a.lstQTR_CO_AMT) as lstQTR_CO_AMT,
    	sum(a.YTDQTR_CO_AMT) as YTDQTR_CO_AMT,
    	sum(a.YTDQTR_CO) as YTDQTR_CO,
    	sum(a.YTDQTR_IP) as YTDQTR_IP,
    	sum(a.LeadCost) as LeadCost, 
    	 
    	sum(Router_13wk) as Router_13wk,
    	sum(Router_13wk_Raw) as Router_13wk_Raw,
    	sum(Web_13wk) as Web_13wk,
    	sum(case when MarketingChannel = 'web' then Open_13wk else 0 end) as Open_13wk_Web,
    	sum(case when MarketingChannel != 'web' then Open_13wk else 0 end) as Open_13wk_Router,
    	sum(case when MarketingChannel = 'web' then CO_13wk else 0 end) as CO_13wk_Web,
    	sum(case when MarketingChannel != 'web' then CO_13wk else 0 end) as CO_13wk_Router,
    	
    	case when sum(Router_13wk)<=10 then 0 else sum(case when MarketingChannel != 'web' then Open_13wk else 0 end)*1.0/sum(Router_13wk) end as RouterCapture,
    	case when sum(Web_13wk)<=10 then 0 else sum(case when MarketingChannel = 'web' then Open_13wk else 0 end)*1.0/sum(Web_13wk) end as WebCapture ,
    	case when sum(Router_13wk_Raw)<=10 then 0 else sum(case when MarketingChannel != 'web' then CO_13wk else 0 end)*1.0/sum(Router_13wk_Raw) end as RouterCloseRatio,
    	case when sum(Web_13wk)<=10 then 0 else sum(case when MarketingChannel = 'web' then CO_13wk else 0 end)*1.0/sum(Web_13wk) end as WebCloseRatio,
    	case when sum(Pitch_13wk)<=10 then 0 else  sum(AO_13wk)* 1.0/sum(Pitch_13wk) end as PitchToAO,
    	
    	case when sum(Router_5wk)<=10 then 0 else sum(case when MarketingChannel != 'web' then Open_5wk else 0 end)*1.0/sum(Router_5wk) end as RouterCapture_5wk,
    	case when sum(Web_5wk)<=10 then 0 else sum(case when MarketingChannel = 'web' then Open_5wk else 0 end)*1.0/sum(Web_5wk) end as WebCapture_5wk		
    from AEMatrix_Report_1  as a 
    where a.WaterFallDivision in 
    	(select division_desc from test_yang.dbo.topdownAELookuptable
    	 where email = 'aaa@aaa.com')		 
    group by  a.WaterFallDivision ,personid
	having sum(Router_13wk_Raw+Web_13wk)>=100      
  """
  query = query.replace('aaa@aaa.com',user_email)  

  queryResult = sql.read_sql(query, cnxn)
  
  xxx= queryResult.mean()  
  
  return xxx 


if __name__ == "__main__":
  user_email = 'btaylor@newdayusa.com'
  queryResult = get_ytdData_bm (user_email)
  xxx= queryResult.mean()  
  xxx= pd.Series.to_frame (xxx) 
  xxx.loc["CO_13wk_Web"][0]