import pyodbc 
import pandas.io.sql as sql

def remove_CO_CRMLoan(all_loans):
  #user_email = 'btaylor@newdayusa.com'
  server = '10.203.1.105\\alpha' 
  database = 'test_yang' 
  username = 'webuser' 
  password = 'Changeme1' 
  cnxn = pyodbc.connect('DRIVER={ODBC Driver 13 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
  

  for i in all_loans:
    sql_code = """ 
      if exists (
      select * from DashboardReport_LoanStatus_CO_CRMs
      where loannum = 'abcdefg'
      ) 
      begin
        insert into DashboardReport_LoanStatus_CO_CRMs_Exceptions
        select * from DashboardReport_LoanStatus_CO_CRMs
        where loannum = 'abcdefg'
      end
      else begin
        insert into DashboardReport_LoanStatus_CO_CRMs_Exceptions
        select 'abcdefg','Good'  
      end      

      delete DashboardReport_LoanStatus_CO_CRMs_Exceptions
      where LoanNum in ('csrfmiddlewaretoken','note_title'); 

      update DashboardReport_LoanStatus_1
        set Comments = 'Good',
        Comments1='',
        Comments2='',
        Comments3='',
        Comments4='',
        Comments5=''	
      where LoanNum  = 'abcdefg'     
    """
    sql_code = sql_code.replace('abcdefg',i)  
    cursor = cnxn.cursor()
    cursor.execute(sql_code)
    cnxn.commit()

  

 
   
  
 