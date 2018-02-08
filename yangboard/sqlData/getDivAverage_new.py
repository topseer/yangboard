import pyodbc 
import pandas.io.sql as sql
from .. import views
from datetime import datetime 


def getDivAverage():
 
  server = '10.203.1.105\\alpha' 
  database = 'test_yang' 
  username = 'webuser' 
  password = 'Changeme1' 
  cnxn = pyodbc.connect('DRIVER={ODBC Driver 13 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
  
  query = """
      with DivAVGs as 
      (
      		select WaterFallDivision,
      			   avg([Router Call]+[Transfer In]-[Transfer Out]+[Web Lead]) as Leads_AVG,
      			   avg([Capture]) as Capture_AVG,
      			   avg(Pitch) as Pitch_AVG,
      			   avg(AO) as AO_AVG,
      			   avg(fund) as Fund_AVG,
      			   'Top20' as Category
      		from DashboardReport_________DivisionActivityBenchMark_2 as a 		
      		where Top20 ='Yes'
      		group by WaterFallDivision
      
      		union 
      
      		select WaterFallDivision,
      			   avg([Router Call]+[Transfer In]-[Transfer Out]+[Web Lead]) as Leads_AVG,
      			   avg([Capture]) as Capture_AVG,
      			   avg(Pitch) as Pitch_AVG,
      			   avg(AO) as AO_AVG,
      			   avg(fund) as Fund_AVG,
      			   'Top50' as Category
      		from DashboardReport_________DivisionActivityBenchMark_2
      		where Top50 ='Yes'
      		group by WaterFallDivision
      )
      select a.*, [Router Call]+[Transfer In]-[Transfer Out]+[Web Lead] as MyLeads,
      	   c.*,lower(b.Email) Email
      from DashboardReport_________DivisionActivityBenchMark_2 as a 
      inner join topDownAELookupTable as b 
      on a.PersonID = b.PersonId      
      inner join DivAVGs as c
      on a.WaterFallDivision = c.WaterFallDivision
  """
  
  queryResult = sql.read_sql(query, cnxn)
  return queryResult
  


      #user_email = "BTAYLOR@NEWDAYUSA.COM"
#      queryResult = views.global_getDivAverage
 #     queryResult = queryResult.loc[queryResult["Email"]==user_email]  
  #    top20 = queryResult.loc[queryResult["Category"]=="Top20",["Leads_AVG","Capture_AVG","Pitch_AVG","AO_AVG","Fund_AVG"]]
   #   top50 = queryResult.loc[queryResult["Category"]=="Top50",["Leads_AVG","Capture_AVG","Pitch_AVG","AO_AVG","Fund_AVG"]]
    #  myself = queryResult.loc[queryResult["Category"]=="Top20",["MyLeads","Capture","Pitch","AO","Fund"]]
     # return list(top20.as_matrix()[0]), list(top50.as_matrix()[0]), list(myself.as_matrix()[0])

   

  
  


           