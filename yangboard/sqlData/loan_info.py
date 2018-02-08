import pyodbc 
import pandas.io.sql as sql
import numpy as np


def get_LoanInfo(loan_number):
  #loan_number = '1213498'
  server = '10.203.1.105\\alpha' 
  database = 'test_yang' 
  username = 'webuser' 
  password = 'Changeme1' 
  cnxn = pyodbc.connect('DRIVER={ODBC Driver 13 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
  
  query = """  
    select LoanNum, FstNm, LstNm, IntRate, FICOScore, HmSt, LoanAmt,b.savings,a.AmortTerm
    from  REPORTS_LS_DM.dbo.Secondary as a 
	inner join [lsprodreports].Reports.dbo.vw_Loan_Info as b 
	on a.loanNum = b.loan_number
    where LoanNum = 'aaaaaaaa'
	and b.loan_number = 'aaaaaaaa'
  """
  query = query.replace('aaaaaaaa',loan_number)  

  queryResult = sql.read_sql(query, cnxn)
    
  queryResult.loc[len(queryResult)] = ["LoanNum","FstNm","LstNm","IntRate","Fico","State","Amt","savings","Term"]
  
  if len(queryResult) > 1 :    
    principal = queryResult["LoanAmt"][0]
    interest_rate  = queryResult["IntRate"][0]/100  
    term = queryResult["AmortTerm"][0]
    
    per = np.arange(term) + 1
    
    ipmt = np.ipmt(interest_rate/12, per, term, principal)
    ppmt = np.ppmt(interest_rate/12, per, term, principal)
    pmt = np.pmt(interest_rate/12, term, principal)
      
    saving = queryResult["savings"][0] 
    PrepaymentStartYear = 3
        
    principal1 = principal 
    ipmt1 = []
    ppmt1 = []
    pmt1 = []
    lastPaymentMonth = 0 
    
    
    for payment in per:
         index = payment - 1
         if payment> PrepaymentStartYear * 12:
             total_pay = -pmt + saving
             InterestPayment = principal1 * interest_rate /12 
         else:
             total_pay = -pmt
             InterestPayment = principal1 * interest_rate /12        
         
         if total_pay>=principal1: 
             total_pay = principal1 + InterestPayment
             if lastPaymentMonth==0:  lastPaymentMonth = payment
              
         PrincipalPayment = total_pay - InterestPayment 
         principal1 = principal1 -  PrincipalPayment
         
         ipmt1 = np.append(ipmt1,InterestPayment)
         ppmt1 = np.append(ppmt1,PrincipalPayment)
         pmt1 = np.append(pmt1,total_pay)
                       
    
    
    total_int_saved ="$"+ str( round(ipmt.sum() *-1 - ipmt1.sum() ,0)).replace(".0","")
     
    erate1 = str(round(np.rate (lastPaymentMonth,(principal + ipmt1.sum())/lastPaymentMonth, -principal,0    )*12*100 , 2))
    
    erate2 = str(round(np.rate (term,(principal + ipmt1.sum())/30/12, -principal,0    )*12*100,2))
    
    lastPaymentYear = str(round(lastPaymentMonth/12,1))
    
    lastPaymentMonth = str(lastPaymentMonth)
     
    return queryResult,total_int_saved,erate1,erate2,lastPaymentYear,lastPaymentMonth
  
  else:
    return queryResult, '0.0','0.0','0.0','1900','01'
           
  
  