from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.views import login
import pyodbc 
import pandas 
import pandas.io.sql as sql
from django import forms
import datetime   
from datetime import date 
from django.shortcuts import redirect

from django.http import JsonResponse
from . import forms
from .forms import NameForm
from .forms import NoteForm
#from .forms import PeriodFilter
from random import randint
from django.views.generic import TemplateView
from datetime import datetime, timedelta
from django.contrib.staticfiles.templatetags.staticfiles import static
import json
import locale
locale.setlocale( locale.LC_ALL, '' )


from .sqlData import ytd_data
from .sqlData import AE_Pipeline
from .sqlData import getEfficiency
from .sqlData import ytd_data_benchmark
from .sqlData import ytd_ranking
from .sqlData import ytd_ranking_div
from .sqlData import AE_Pipeline_Count
from .sqlData import getDivAverage
from .sqlData import get_myTeam
from .sqlData import data_LeadsVolume
from .sqlData import datatrend
from .sqlData import getDivAverage_new
from .sqlData import datatrend_new
from .sqlData import getEfficiency_new
from .sqlData import ytd_data_new
from .sqlData import loan_info 


lstRunTime = datetime(2018, 1, 2, 1, 1, 1, 1)
global_getDivAverage = getDivAverage_new.getDivAverage ()   
global_activity_rawdata = datatrend_new.datatrend ()   
global_efficiency_rawdata = getEfficiency_new. getEfficiency()
global_ytd_data = ytd_data_new. get_ytdData()


def refresh_data(user_email):  
    global lstRunTime
    currentTime = datetime.now()
    currentTime_to_LstRunTime =  (currentTime - lstRunTime).days*24*60 + (currentTime - lstRunTime).seconds/60
    
    if currentTime_to_LstRunTime>=60:
      lstRunTime = datetime.now()     
      global global_getDivAverage 
      global global_activity_rawdata 
      global global_efficiency_rawdata
      global global_ytd_data
      
      global_activity_rawdata = datatrend_new.datatrend ()   
      global_getDivAverage = getDivAverage_new.getDivAverage ()   
      global_efficiency_rawdata = getEfficiency_new. getEfficiency()          
      global_ytd_data = ytd_data_new. get_ytdData()


def HomePage(request):
    if request.user.is_authenticated:
                       
        isAVP= request.user.groups.filter(name__in=['avp','AVP']).exists()                                
        isPrch  = request.user.groups.filter(name__in=['Purchase']).exists()   
        user = request.user
        user_email = user.email.lower()
        myteam = get_myTeam.get_myTeam(user_email)                             
        img_url = 'img.jpg'
        
        salesQuote = ['You will never find time for anything. If you want time you must make it. – Charles Robert Buxton',
                      'The difference between a successful person and others is not a lack of strength, not a lack of knowledge, but rather a lack of will. – Vince Lombardi',                      
                      'The difference between try and triumph is just a little umph! – Marvin Phillips',
                      'Every brand isn’t for everybody, and everybody isn’t for every brand. – Liz Lange',
                      'The most unprofitable item ever manufactured is an excuse. – John Mason',
                      'Success is the culmination of failures, mistakes, false starts, confusion, and the determination to keep going anyway. – Nick Gleason',
                      'Most people think selling is the same as talking. But the most effective salespeople know that listening is the most important part of their job.',
                      'You dont close a sale; you open a relationship if you want to build a long-term, successful enterprise. – Patricia Fripp',
                      'If you are not taking care of your customer, your competitor will. – Bob Hooey',
                      'There are no shortcuts to any place worth going. – Beverly Sills',
                      'Life’s battles don’t always go to the strongest or fastest; sooner or later those who win are those who think they can. – Richard Bach'
        ]
        return render(request, 'HomePage.html',
                    context={                        
                             'salesQuote':salesQuote,                     
                             'img_url':img_url,
                             'isAVP':isAVP,
                             'isPrch':isPrch,       
                             'myteam':myteam,                 
                            },
         ) 
    else:       
       return  redirect('accounts/login/')
    # return render(
    #     request, 
    #      'GDashboard/production/index.html',
    #      context={'num_leads_yst':num_Router_lstWk,'user_email':user_email,'form':form},
    #      ) 


  
    
def dashboard(request):
    if request.user.is_authenticated:
        
        
        loanNumber = request.GET.get('loanNumber')            
        
        if loanNumber == None: loanNumber = "XXXXXXX"
        
        my_loaninfo,total_int_saved,erate1,erate2,lastPaymentYear,lastPaymentMonth = loan_info.get_LoanInfo(loanNumber)
        
        my_loaninfo_fstnm = my_loaninfo["FstNm"][0]
        my_loaninfo_lstnm = my_loaninfo["LstNm"][0]
        my_loaninfo_intrate = my_loaninfo["IntRate"][0]
        my_loaninfo_fico = my_loaninfo["FICOScore"][0]
        my_loaninfo_LoanAmt = my_loaninfo["LoanAmt"][0]
                
            
        user = request.user
        user_email = user.email.lower()
        
        isAVP = request.user.groups.filter(name__in=['avp','AVP']).exists()         
        isPrch = request.user.groups.filter(name__in=['Purchase']).exists()                                 

        myteam = get_myTeam.get_myTeam(user_email)


        refresh_data(user_email)
        
        
        
        ##get activities data 
        #activity_top20,activity_top50,activity_myself = getDivAverage.getDivAverage (user_email)
        global_getDivAverage_user = global_getDivAverage.loc[global_getDivAverage["Email"]==user_email]  

        if len(global_getDivAverage_user)==0: 
          activity_top20 = [0]
          activity_top50 = [0]
          activity_myself = [0]
        else: 
          activity_top20 = list(global_getDivAverage_user.loc[global_getDivAverage_user["Category"]=="Top20",["Leads_AVG","Capture_AVG","Pitch_AVG","AO_AVG","Fund_AVG"]].as_matrix()[0])
          activity_top50 = list(global_getDivAverage_user.loc[global_getDivAverage_user["Category"]=="Top50",["Leads_AVG","Capture_AVG","Pitch_AVG","AO_AVG","Fund_AVG"]].as_matrix()[0])
          activity_myself = list(global_getDivAverage_user.loc[global_getDivAverage_user["Category"]=="Top20",["MyLeads","Capture","Pitch","AO","Fund"]].as_matrix()[0])
            
        if len(activity_top20)==0:
          activity_top20 = [0]
          activity_top50 = [0]
          activity_myself = [0]
          
                    
        #charts of activity
        #activity_rawdata = datatrend.datatrend(user_email)                        
        activity_rawdata = global_activity_rawdata.loc[global_activity_rawdata["Email"]==user_email]  
        activity_rawdata = activity_rawdata.sort_values(["StartOfWeek_Date"])
        
         
         
         
        if len(activity_rawdata)>0:
          timeseries_totalLeads = (activity_rawdata["WebLead"] +activity_rawdata["RouterCall"] + activity_rawdata["TransferIn"] - activity_rawdata["TransferOut"]).tolist()
          timeseries_AOs = activity_rawdata["AO"].tolist()
          timeseries_opens = activity_rawdata["Capture"].tolist()
          timeseries_pitches = activity_rawdata["Pitch"].tolist()                
          timeseries_tiemRange = activity_rawdata["StartOfWeek"].tolist()
        else: 
          timeseries_totalLeads = [0]
          timeseries_AOs = [0]
          timeseries_opens = [0]
          timeseries_pitches = [0]
          timeseries_tiemRange = [0]


          
        #efficiency data
        #efficiency_rawdata = getEfficiency.getEfficiency(user_email)
        efficiency_rawdata = global_efficiency_rawdata.loc[global_efficiency_rawdata["Email"]==user_email,]        
        if len(efficiency_rawdata)>0:
          RouterCapture13wk = efficiency_rawdata["Router Capture 13wk"].iloc[0]
          WebCapture13wk = efficiency_rawdata["Web Capture 13wk"].iloc[0]
          RouterClose13wk = efficiency_rawdata["Router Close 13wk"].iloc[0]
          WebClose13wk = efficiency_rawdata["Web Close 13wk"].iloc[0]
          Open_to_pich_13wk = efficiency_rawdata["Open-Pitch 13wk"].iloc[0]
          Pitch_to_AO_13wk = efficiency_rawdata["Pitch-AO 13wk"].iloc[0]
          RouterCapture13wk_bm = efficiency_rawdata["Router Capture BM"].iloc[0]
          WebCapture13wk_bm = efficiency_rawdata["Web Capture BM"].iloc[0]
          RouterClose13wk_bm = efficiency_rawdata["Router Close BM"].iloc[0]
          WebClose13wk_bm = efficiency_rawdata["Web Close BM"].iloc[0]
          Open_to_pich_13wk_bm = efficiency_rawdata["Open-Pitch BM"].iloc[0]
          Pitch_to_AO_13wk_bm = efficiency_rawdata["Pitch-AO BM"].iloc[0]
          
          RouterCapture13wk_Rel= RouterCapture13wk / (RouterCapture13wk_bm+0.0001) * 100
          WebCapture13wk_Rel= WebCapture13wk / (WebCapture13wk_bm+0.0001) * 100
          RouterClose13wk_Rel= RouterClose13wk / (RouterClose13wk_bm+0.0001) * 100
          WebClose13wk_Rel= WebClose13wk /( WebClose13wk_bm+0.0001) * 100
          Open_to_pich_13wk_Rel= Open_to_pich_13wk / (Open_to_pich_13wk_bm+0.0001) * 100
          Pitch_to_AO_13wk_Rel= Pitch_to_AO_13wk / (Pitch_to_AO_13wk_bm+0.0001) * 100
                  
          RouterCapture13wk_bm_Rel = 100
          WebCapture13wk_bm_Rel = 100
          RouterClose13wk_bm_Rel = 100
          WebClose13wk_bm_Rel = 100
          Open_to_pich_13wk_bm_Rel = 100
          Pitch_to_AO_13wk_bm_Rel = 100
        else:
          RouterCapture13wk_bm_Rel = 100
          WebCapture13wk_bm_Rel = 100
          RouterClose13wk_bm_Rel = 100
          WebClose13wk_bm_Rel = 100
          Open_to_pich_13wk_bm_Rel = 100
          Pitch_to_AO_13wk_bm_Rel = 100
          RouterCapture13wk_Rel= 120
          WebCapture13wk_Rel= 120
          RouterClose13wk_Rel= 120
          WebClose13wk_Rel= 120
          Open_to_pich_13wk_Rel= 120
          Pitch_to_AO_13wk_Rel= 120
          RouterCapture13wk = 0 
          WebCapture13wk = 0 
          WebClose13wk = 0 
          Pitch_to_AO_13wk = 0
          Open_to_pich_13wk = 0 
          RouterClose13wk = 0 

        #the top section: check ytdData is not null!!!
        test_123 = ''
        
        ytdData = global_ytd_data.loc[global_ytd_data["Email"]==user_email,]
        #ytdData = ytd_data.get_ytdData (user_email)   
        
        if len(ytdData)>0:
          YTDQTR_CO = ytdData["YTDQTR_CO"].iloc[0].astype(int)
          YTDQTR_CO_AMT_raw =  ytdData["YTDQTR_CO_AMT"].iloc[0].astype(int)
          YTDQTR_CO_AMT =  locale.currency (ytdData["YTDQTR_CO_AMT"].iloc[0].astype(int), grouping=True )
          YTDQTR_CO_AMT =  YTDQTR_CO_AMT [:-3]
          CurrQTR_CO_AMT_raw = ytdData["CurrQTR_CO_AMT"].iloc[0].astype(int)
          CurrQTR_CO_AMT = locale.currency (ytdData["CurrQTR_CO_AMT"].iloc[0].astype(int), grouping = True)
          CurrQTR_CO_AMT =  CurrQTR_CO_AMT [:-3]
          lstQTR_CO_AMT_raw = ytdData["lstQTR_CO_AMT"].iloc[0].astype(int)
          lstQTR_CO_AMT = locale.currency (ytdData["lstQTR_CO_AMT"].iloc[0].astype(int), grouping = True)
          lstQTR_CO_AMT = lstQTR_CO_AMT [:-3]
          CO_CLose = ytdData["CO Close"].iloc[0].astype(int)
          AE_Ranking = ytdData["Ranking"].iloc[0].astype(int)
        else:
          YTDQTR_CO = 100
          YTDQTR_CO_AMT_raw =  100
          YTDQTR_CO_AMT =  100
          CurrQTR_CO_AMT_raw = 100
          CurrQTR_CO_AMT =  100
          lstQTR_CO_AMT_raw = 100
          lstQTR_CO_AMT = 100
          CO_CLose = 100
          AE_Ranking = 100
        
        
        LeadsVolume_Data = data_LeadsVolume.get_LeadsVolume()
        if len (LeadsVolume_Data) > 0 :
          LeadsVolume_Time = LeadsVolume_Data["time"].tolist()
          LeadsVolume_Projected = LeadsVolume_Data["Projected"].tolist()
          LeadsVolume_Calls = LeadsVolume_Data["Calls"].tolist()
          LeadsVolume_WebLeads = LeadsVolume_Data["WebLeads"].tolist()
          LeadsVolume_TotalCalls = LeadsVolume_Data["TotalCalls"].tolist()
        else: 
          LeadsVolume_Time = [0]
          LeadsVolume_Projected = [0]
          LeadsVolume_Calls = [0]
          LeadsVolume_WebLeads = [0]
          LeadsVolume_TotalCalls = [0]          

        ytdData_bm = ytd_data_benchmark.get_ytdData_bm (user_email)      
        if len(ytdData)>0:
          BM_YTDQTR_CO = ytdData_bm["YTDQTR_CO"] 
          BM_YTDQTR_CO_AMT_raw =  ytdData_bm["YTDQTR_CO_AMT"] 
          BM_CurrQTR_CO_AMT_raw = ytdData_bm["CurrQTR_CO_AMT"] 
          BM_lstQTR_CO_AMT_raw = ytdData_bm["lstQTR_CO_AMT"]
          BM_CO_CLose = ytdData_bm["CO Close"]          
        else:
          BM_YTDQTR_CO = 100
          BM_YTDQTR_CO_AMT_raw =  100        
          BM_CurrQTR_CO_AMT_raw =  100          
          BM_lstQTR_CO_AMT_raw = 100
          BM_CO_CLose = 100

        ytdRank = ytd_ranking.get_ytdranking(user_email)
        ytdRank_div = ytd_ranking_div.get_ytdranking_div(user_email)
        if len(ytdRank)>0:
          myRank = ytdRank["Ranking"][0]          
          myDiff = '{0:g}'.format( round(ytdRank["YCOhead"][0]) - round(ytdRank["YTDQTR_CO"][0]))
          myRankHead = '{0:g}'.format( ytdRank["Ranking"][0] - 1)          
        else:
          myRank = 1
          myDiff = "You are the Number 1"
          myRankHead = 1

        if len(ytdRank_div)>0:
          myRank_div = ytdRank_div["Ranking"][0]          
          myDiff_div = '{0:g}'.format( round(ytdRank_div["YCOhead"][0]) - round(ytdRank_div["YTDQTR_CO"][0]))
          myRankHead_div = '{0:g}'.format( ytdRank_div["Ranking"][0] - 1)          
        
        else:
          myDiff_div = "You are the Number 1"
          myRank_div = 1
          myRankHead_div = 1
 
        YTDQTR_CO_Diff = round( (YTDQTR_CO - BM_YTDQTR_CO)/ BM_YTDQTR_CO * 100 ,1) 
        YTDQTR_CO_AMT_Diff = round(  (YTDQTR_CO_AMT_raw - BM_YTDQTR_CO_AMT_raw)/ BM_YTDQTR_CO_AMT_raw * 100,1)
        CurrQTR_CO_AMT_Diff = round(  (CurrQTR_CO_AMT_raw - BM_CurrQTR_CO_AMT_raw)/ BM_CurrQTR_CO_AMT_raw * 100,1)
        lstQTR_CO_AMT_Diff = round(  (lstQTR_CO_AMT_raw - BM_lstQTR_CO_AMT_raw)/ BM_lstQTR_CO_AMT_raw * 100,1)
        CO_CLose_Diff =  round( (CO_CLose - BM_CO_CLose)/ BM_CO_CLose * 100,1)
        

        ae_pipeline_sum = AE_Pipeline_Count.get_AEPipeline_Count(user_email)

        if len(ae_pipeline_sum)>0:
          myPip = ae_pipeline_sum["Pip"][0]            
          myIP = ae_pipeline_sum["IP"][0]            
          myTotalLoans = ae_pipeline_sum["TotalPipe"][0]            
        else:
          myPip = 1
          myIP = 1
          myTotalLoans = 2

        #pipe
        aePipeline = AE_Pipeline.get_AEPipeline(user_email)         
        aePipeline_json = json.dumps(aePipeline)
        
        #pic
        img_url = 'img.jpg'
        
        salesQuote = ['You will never find time for anything. If you want time you must make it. – Charles Robert Buxton',
                      'The difference between a successful person and others is not a lack of strength, not a lack of knowledge, but rather a lack of will. – Vince Lombardi',                      
                      'The difference between try and triumph is just a little umph! – Marvin Phillips',
                      'Every brand isn’t for everybody, and everybody isn’t for every brand. – Liz Lange',
                      'The most unprofitable item ever manufactured is an excuse. – John Mason',
                      'Success is the culmination of failures, mistakes, false starts, confusion, and the determination to keep going anyway. – Nick Gleason',
                      'Most people think selling is the same as talking. But the most effective salespeople know that listening is the most important part of their job.',
                      'You dont close a sale; you open a relationship if you want to build a long-term, successful enterprise. – Patricia Fripp',
                      'If you are not taking care of your customer, your competitor will. – Bob Hooey',
                      'There are no shortcuts to any place worth going. – Beverly Sills',
                      'Life’s battles don’t always go to the strongest or fastest; sooner or later those who win are those who think they can. – Richard Bach'
        ]
        return render(request, 'dashboard.html',
                    context={
                             'test_test':str(lstRunTime),
                             'test_123':test_123,
                             'salesQuote':salesQuote,
                             'user_email':user_email,        
                             'isAVP':isAVP,
                             'isPrch':isPrch,
                             'myteam':myteam,      
                             
                             
                             'loanNumber':loanNumber,
                             'my_loaninfo_fstnm':my_loaninfo_fstnm,
                             'my_loaninfo_lstnm':my_loaninfo_lstnm ,
                             'my_loaninfo_intrate':my_loaninfo_intrate,
                             'my_loaninfo_fico':my_loaninfo_fico ,
                             'my_loaninfo_LoanAmt':my_loaninfo_LoanAmt ,
                             'total_int_saved':total_int_saved,
                             'erate1':erate1,
                             'erate2':erate2,
                             'lastPaymentYear':lastPaymentYear,
                             'lastPaymentMonth':lastPaymentMonth,        
                             
                             'YTDQTR_CO':YTDQTR_CO ,     
                             'YTDQTR_CO_AMT':YTDQTR_CO_AMT ,     
                             'CurrQTR_CO_AMT':CurrQTR_CO_AMT ,     
                             'lstQTR_CO_AMT':lstQTR_CO_AMT ,     
                             'CO_CLose':CO_CLose ,     
                             
                             'AE_Ranking': myRank,                             
                             "myRankHead": myRankHead,
                             'AE_Ranking_div': myRank_div,
                             "myRankHead_div": myRankHead_div,       
                             
                             'activity_top20': activity_top20,
                             'activity_top50' : activity_top50,
                             'activity_myself': activity_myself,
                             'aePipeline_js':aePipeline,
                             'aePipeline_json':aePipeline_json,
                             
                             'timeseries_totalLeads':timeseries_totalLeads,
                             'timeseries_AOs':timeseries_AOs,
                             'timeseries_opens':timeseries_opens,
                             'timeseries_pitches':timeseries_pitches,
                             'timeseries_tiemRange':timeseries_tiemRange,

                             'LeadsVolume_Time':LeadsVolume_Time,
                             'LeadsVolume_Projected':LeadsVolume_Projected,
                             'LeadsVolume_Calls':LeadsVolume_Calls,
                             'LeadsVolume_WebLeads':LeadsVolume_WebLeads,
                             'LeadsVolume_TotalCalls':LeadsVolume_TotalCalls,
      

                             'RouterCapture13wk_Rel':RouterCapture13wk_Rel,
                             'WebCapture13wk_Rel':WebCapture13wk_Rel,
                             'RouterClose13wk_Rel':RouterClose13wk_Rel,
                             'WebClose13wk_Rel':WebClose13wk_Rel,
                             'Open_to_pich_13wk_Rel':Open_to_pich_13wk_Rel,
                             'Pitch_to_AO_13wk_Rel':Pitch_to_AO_13wk_Rel,

                             'RouterCapture13wk_bm_Rel':RouterCapture13wk_bm_Rel,
                             'WebCapture13wk_bm_Rel':WebCapture13wk_bm_Rel,
                             'RouterClose13wk_bm_Rel':RouterClose13wk_bm_Rel,
                             'WebClose13wk_bm_Rel':WebClose13wk_bm_Rel,
                             'Open_to_pich_13wk_bm_Rel':Open_to_pich_13wk_bm_Rel,
                             'Pitch_to_AO_13wk_bm_Rel':Pitch_to_AO_13wk_bm_Rel,
                             'img_url':img_url,
                             'YTDQTR_CO_Diff':YTDQTR_CO_Diff,
                              'YTDQTR_CO_AMT_Diff' :YTDQTR_CO_AMT_Diff,
                              'CurrQTR_CO_AMT_Diff'  :CurrQTR_CO_AMT_Diff,
                              'lstQTR_CO_AMT_Diff'   :lstQTR_CO_AMT_Diff,
                              'CO_CLose_Diff'     :CO_CLose_Diff    ,
                              'myPip':myPip    ,
                              'myIP':myIP    ,
                              'myTotalLoans':myTotalLoans    ,
                              'myDiff':myDiff    ,
                              'RouterCapture13wk':RouterCapture13wk    ,
                              'WebCapture13wk':WebCapture13wk    ,
                              'RouterClose13wk':RouterClose13wk    ,
                              'WebClose13wk':WebClose13wk    ,
                              'Open_to_pich_13wk':Open_to_pich_13wk    ,
                              'Pitch_to_AO_13wk':Pitch_to_AO_13wk    

                            },
         ) 
    else:       
       return  redirect('accounts/login/')
    # return render(
    #     request, 
    #      'GDashboard/production/index.html',
    #      context={'num_leads_yst':num_Router_lstWk,'user_email':user_email,'form':form},
    #      ) 


def myPipeline(request):
    if request.user.is_authenticated:
        user = request.user

        isAVP = request.user.groups.filter(name__in=['avp','AVP']).exists()         
        isPrch = request.user.groups.filter(name__in=['Purchase']).exists()               

        user_email = user.email.lower()        

        myteam = get_myTeam.get_myTeam(user_email)

        refresh_data(user_email)
        myNoteContent = ""
        note_appointment = ""

        if request.method == 'POST':                                
          myNoteForm = NoteForm(request.POST)          
          
          if myNoteForm.is_valid():            
            myNoteContent = myNoteForm.cleaned_data['note_title']
            myNoteForm = NoteForm()
        
        else:
          myNoteForm = NoteForm()
              
        ae_pipeline_sum = AE_Pipeline_Count.get_AEPipeline_Count(user_email,isPrch)

        if len(ae_pipeline_sum)>0:
          myPip = ae_pipeline_sum["Pip"][0]            
          myIP = ae_pipeline_sum["IP"][0]            
          myTotalLoans = ae_pipeline_sum["TotalPipe"][0]            
        else:
          myPip = 0
          myIP = 0
          myTotalLoans = 0

        #pipe
        aePipeline, aePipeline_PreQual= AE_Pipeline.get_AEPipeline(user_email,isPrch)     
                        

        #pic
        img_url = 'img.jpg'
        
        salesQuote = ['You will never find time for anything. If you want time you must make it. – Charles Robert Buxton',
                      'The difference between a successful person and others is not a lack of strength, not a lack of knowledge, but rather a lack of will. – Vince Lombardi',                      
                      'The difference between try and triumph is just a little umph! – Marvin Phillips',
                      'Every brand isn’t for everybody, and everybody isn’t for every brand. – Liz Lange',
                      'The most unprofitable item ever manufactured is an excuse. – John Mason',
                      'Success is the culmination of failures, mistakes, false starts, confusion, and the determination to keep going anyway. – Nick Gleason',
                      'Most people think selling is the same as talking. But the most effective salespeople know that listening is the most important part of their job.',
                      'You dont close a sale; you open a relationship if you want to build a long-term, successful enterprise. – Patricia Fripp',
                      'If you are not taking care of your customer, your competitor will. – Bob Hooey',
                      'There are no shortcuts to any place worth going. – Beverly Sills',
                      'Life’s battles don’t always go to the strongest or fastest; sooner or later those who win are those who think they can. – Richard Bach'
        ]

        if (isPrch): 
              return render(request, 'myPipeline_prch.html',
                    context={
                              'myNoteForm':myNoteForm,
                              'myNoteContent':myNoteContent,
                              'myPip':myPip    ,
                              'myIP':myIP    ,
                              'myTotalLoans':myTotalLoans  ,
                              'salesQuote':salesQuote,
                              'user_email':user_email,    
                              'img_url':img_url, 
                              'aePipeline_js':aePipeline,                                     
                              'aePipeline_PreQual_js':aePipeline_PreQual,                                 
                              'myteam':myteam,       
                              'isAVP':isAVP,
                              'isPrch':isPrch
                            },
              ) 
        else: return render(request, 'myPipeline.html',
                    context={
                              'myNoteForm':myNoteForm,
                              'myNoteContent':myNoteContent,
                              'myPip':myPip    ,
                              'myIP':myIP    ,
                              'myTotalLoans':myTotalLoans  ,
                              'salesQuote':salesQuote,
                              'user_email':user_email,    
                              'img_url':img_url, 
                              'aePipeline_js':aePipeline,                                         
                              'aePipeline_PreQual_js':aePipeline_PreQual,                                 
                              'myteam':myteam,       
                              'isAVP':isAVP,
                              'isPrch':isPrch
                            },
              ) 
    else:       
       return  redirect('accounts/login/')
  



def my_team_member_pipeline(request,team_member_email):
    if request.user.is_authenticated:
        user = request.user
        user_email = user.email.lower()
        isAVP = request.user.groups.filter(name__in=['avp','AVP']).exists()         
        isPrch = request.user.groups.filter(name__in=['Purchase']).exists()               
        myteam = get_myTeam.get_myTeam(user_email)    

        user_email = team_member_email.lower()
                    
        refresh_data(user_email)
        myNoteContent = ""
        note_appointment = ""

        if request.method == 'POST':                                
          myNoteForm = NoteForm(request.POST)          
          
          if myNoteForm.is_valid():            
            myNoteContent = myNoteForm.cleaned_data['note_title']
            myNoteForm = NoteForm()
        
        else:
          myNoteForm = NoteForm()
              

        ae_pipeline_sum = AE_Pipeline_Count.get_AEPipeline_Count(user_email,isPrch)

        if len(ae_pipeline_sum)>0:
          myPip = ae_pipeline_sum["Pip"][0]            
          myIP = ae_pipeline_sum["IP"][0]            
          myTotalLoans = ae_pipeline_sum["TotalPipe"][0]            
        else:
          myPip = 0
          myIP = 0
          myTotalLoans = 0

        #pipe
        aePipeline, aePipeline_PreQual= AE_Pipeline.get_AEPipeline(user_email,isPrch)                
        
        #pic
        img_url = 'img.jpg'


        
        salesQuote = ['You will never find time for anything. If you want time you must make it. – Charles Robert Buxton',
                      'The difference between a successful person and others is not a lack of strength, not a lack of knowledge, but rather a lack of will. – Vince Lombardi',                      
                      'The difference between try and triumph is just a little umph! – Marvin Phillips',
                      'Every brand isn’t for everybody, and everybody isn’t for every brand. – Liz Lange',
                      'The most unprofitable item ever manufactured is an excuse. – John Mason',
                      'Success is the culmination of failures, mistakes, false starts, confusion, and the determination to keep going anyway. – Nick Gleason',
                      'Most people think selling is the same as talking. But the most effective salespeople know that listening is the most important part of their job.',
                      'You dont close a sale; you open a relationship if you want to build a long-term, successful enterprise. – Patricia Fripp',
                      'If you are not taking care of your customer, your competitor will. – Bob Hooey',
                      'There are no shortcuts to any place worth going. – Beverly Sills',
                      'Life’s battles don’t always go to the strongest or fastest; sooner or later those who win are those who think they can. – Richard Bach'
        ]
        
        if (isPrch): 
              return render(request, 'myPipeline_prch.html',
                    context={
                              'myNoteForm':myNoteForm,
                              'myNoteContent':myNoteContent,
                              'myPip':myPip    ,
                              'myIP':myIP    ,
                              'myTotalLoans':myTotalLoans  ,
                              'salesQuote':salesQuote,
                              'user_email':user_email,    
                              'img_url':img_url, 
                              'aePipeline_js':aePipeline,                                     
                              'aePipeline_PreQual_js':aePipeline_PreQual,                                 
                              'myteam':myteam,       
                              'isAVP':isAVP,
                              'isPrch':isPrch
                            },
              ) 
        else: return render(request, 'myPipeline.html',
                    context={
                              'myNoteForm':myNoteForm,
                              'myNoteContent':myNoteContent,
                              'myPip':myPip    ,
                              'myIP':myIP    ,
                              'myTotalLoans':myTotalLoans  ,
                              'salesQuote':salesQuote,
                              'user_email':user_email,    
                              'img_url':img_url, 
                              'aePipeline_js':aePipeline,                                         
                              'aePipeline_PreQual_js':aePipeline_PreQual,                                 
                              'myteam':myteam,       
                              'isAVP':isAVP,
                              'isPrch':isPrch
                            },
              ) 
      
    else:       
       return  redirect('accounts/login/')




def my_team_total_pipeline(request):
    if request.user.is_authenticated:
        user = request.user
        user_email = user.email.lower()
        isAVP = request.user.groups.filter(name__in=['avp','AVP']).exists()         
        isPrch = request.user.groups.filter(name__in=['Purchase']).exists()               
        myteam = get_myTeam.get_myTeam(user_email)    
        
                    
        refresh_data(user_email)
        myNoteContent = ""
        note_appointment = ""
            
        ae_pipeline_sum = AE_Pipeline_Count.get_TeamPipeline_Count(user_email)

        if len(ae_pipeline_sum)>0:
          myPip = ae_pipeline_sum["Pip"][0]            
          myIP = ae_pipeline_sum["IP"][0]            
          myTotalLoans = ae_pipeline_sum["TotalPipe"][0]            
        else:
          myPip = 0
          myIP = 0
          myTotalLoans = 0

        #pipe
        aePipeline = AE_Pipeline.get_TeamPipeline(user_email)         
        aePipeline_json = json.dumps(aePipeline)
        
        #pic
        img_url = 'img.jpg'


        
        salesQuote = ['You will never find time for anything. If you want time you must make it. – Charles Robert Buxton',
                      'The difference between a successful person and others is not a lack of strength, not a lack of knowledge, but rather a lack of will. – Vince Lombardi',                      
                      'The difference between try and triumph is just a little umph! – Marvin Phillips',
                      'Every brand isn’t for everybody, and everybody isn’t for every brand. – Liz Lange',
                      'The most unprofitable item ever manufactured is an excuse. – John Mason',
                      'Success is the culmination of failures, mistakes, false starts, confusion, and the determination to keep going anyway. – Nick Gleason',
                      'Most people think selling is the same as talking. But the most effective salespeople know that listening is the most important part of their job.',
                      'You dont close a sale; you open a relationship if you want to build a long-term, successful enterprise. – Patricia Fripp',
                      'If you are not taking care of your customer, your competitor will. – Bob Hooey',
                      'There are no shortcuts to any place worth going. – Beverly Sills',
                      'Life’s battles don’t always go to the strongest or fastest; sooner or later those who win are those who think they can. – Richard Bach'
        ]
        return render(request, 'my_Team_Pipeline.html',
                    context={                              
                              'myNoteContent':myNoteContent,
                              'myPip':myPip    ,
                              'myIP':myIP    ,
                              'myTotalLoans':myTotalLoans  ,
                              'salesQuote':salesQuote,
                              'user_email':user_email,    
                              'img_url':img_url, 
                              'aePipeline_js':aePipeline,
                              'aePipeline_json':aePipeline_json,           
                              'myteam':myteam,       
                              'isAVP':isAVP,
                              'isPrch':isPrch
                            },
         ) 
    else:       
       return  redirect('accounts/login/')






def my_team_member(request,team_member_email):
    if request.user.is_authenticated:
        
        user_email = team_member_email
        
        isAVP = request.user.groups.filter(name__in=['avp','AVP']).exists()        
        myteam = get_myTeam.get_myTeam(user_email)
 
        activity_top20,activity_top50,activity_myself = getDivAverage.getDivAverage (user_email)
        
        if len(activity_top20)==0:
          activity_top20 = [0]
          activity_top50 = [0]
          activity_myself = [0]
          
                    
        #charts of activity
        activity_rawdata = datatrend.datatrend(user_email)        
        if len(activity_rawdata)>0:
          timeseries_totalLeads = (activity_rawdata["WebLead"] +activity_rawdata["RouterCall"] + activity_rawdata["TransferIn"] - activity_rawdata["TransferOut"]).tolist()
          timeseries_AOs = activity_rawdata["AO"].tolist()
          timeseries_opens = activity_rawdata["Capture"].tolist()
          timeseries_pitches = activity_rawdata["Pitch"].tolist()                
          timeseries_tiemRange = activity_rawdata["StartOfWeek"].tolist()
        else: 
          timeseries_totalLeads = [0]
          timeseries_AOs = [0]
          timeseries_opens = [0]
          timeseries_pitches = [0]
          timeseries_tiemRange = [0]
          
        #efficiency data
        efficiency_rawdata = getEfficiency.getEfficiency(user_email)
        if len(efficiency_rawdata)>0:
          RouterCapture13wk = efficiency_rawdata["Router Capture 13wk"][0]
          WebCapture13wk = efficiency_rawdata["Web Capture 13wk"][0]
          RouterClose13wk = efficiency_rawdata["Router Close 13wk"][0]
          WebClose13wk = efficiency_rawdata["Web Close 13wk"][0]
          Open_to_pich_13wk = efficiency_rawdata["Open-Pitch 13wk"][0]
          Pitch_to_AO_13wk = efficiency_rawdata["Pitch-AO 13wk"][0]
          RouterCapture13wk_bm = efficiency_rawdata["Router Capture BM"][0]
          WebCapture13wk_bm = efficiency_rawdata["Web Capture BM"][0]
          RouterClose13wk_bm = efficiency_rawdata["Router Close BM"][0]
          WebClose13wk_bm = efficiency_rawdata["Web Close BM"][0]
          Open_to_pich_13wk_bm = efficiency_rawdata["Open-Pitch BM"][0]
          Pitch_to_AO_13wk_bm = efficiency_rawdata["Pitch-AO BM"][0]
          
          RouterCapture13wk_Rel= RouterCapture13wk / (RouterCapture13wk_bm+0.0001) * 100
          WebCapture13wk_Rel= WebCapture13wk / (WebCapture13wk_bm+0.0001) * 100
          RouterClose13wk_Rel= RouterClose13wk / (RouterClose13wk_bm+0.0001) * 100
          WebClose13wk_Rel= WebClose13wk /( WebClose13wk_bm+0.0001) * 100
          Open_to_pich_13wk_Rel= Open_to_pich_13wk / (Open_to_pich_13wk_bm+0.0001) * 100
          Pitch_to_AO_13wk_Rel= Pitch_to_AO_13wk / (Pitch_to_AO_13wk_bm+0.0001) * 100
                  
          RouterCapture13wk_bm_Rel = 100
          WebCapture13wk_bm_Rel = 100
          RouterClose13wk_bm_Rel = 100
          WebClose13wk_bm_Rel = 100
          Open_to_pich_13wk_bm_Rel = 100
          Pitch_to_AO_13wk_bm_Rel = 100
          
          if RouterCapture13wk_Rel>=150: RouterCapture13wk_Rel = 150
          if WebCapture13wk_Rel>=150: WebCapture13wk_Rel = 150
          if RouterClose13wk_Rel>=150: RouterClose13wk_Rel = 150
          if WebClose13wk_Rel>=150: WebClose13wk_Rel = 150
          if Open_to_pich_13wk_Rel>=150: Open_to_pich_13wk_Rel = 150
          if Pitch_to_AO_13wk_Rel>=150: Pitch_to_AO_13wk_Rel = 150
          
        else:
          RouterCapture13wk_bm_Rel = 100
          WebCapture13wk_bm_Rel = 100
          RouterClose13wk_bm_Rel = 100
          WebClose13wk_bm_Rel = 100
          Open_to_pich_13wk_bm_Rel = 100
          Pitch_to_AO_13wk_bm_Rel = 100
          RouterCapture13wk_Rel= 120
          WebCapture13wk_Rel= 120
          RouterClose13wk_Rel= 120
          WebClose13wk_Rel= 120
          Open_to_pich_13wk_Rel= 120
          Pitch_to_AO_13wk_Rel= 120


        #the top section: check ytdData is not null!!!
        ytdData = ytd_data.get_ytdData (user_email)      
        if len(ytdData)>0:
          YTDQTR_CO = ytdData["YTDQTR_CO"][0].astype(int)
          YTDQTR_CO_AMT_raw =  ytdData["YTDQTR_CO_AMT"][0].astype(int)
          YTDQTR_CO_AMT =  locale.currency (ytdData["YTDQTR_CO_AMT"][0].astype(int), grouping=True )
          YTDQTR_CO_AMT =  YTDQTR_CO_AMT [:-3]
          CurrQTR_CO_AMT_raw = ytdData["CurrQTR_CO_AMT"][0].astype(int)
          CurrQTR_CO_AMT = locale.currency (ytdData["CurrQTR_CO_AMT"][0].astype(int), grouping = True)
          CurrQTR_CO_AMT =  CurrQTR_CO_AMT [:-3]
          lstQTR_CO_AMT_raw = ytdData["lstQTR_CO_AMT"][0].astype(int)
          lstQTR_CO_AMT = locale.currency (ytdData["lstQTR_CO_AMT"][0].astype(int), grouping = True)
          lstQTR_CO_AMT = lstQTR_CO_AMT [:-3]
          CO_CLose = ytdData["CO Close"][0].astype(int)
          AE_Ranking = ytdData["Ranking"][0].astype(int)
        else:
          YTDQTR_CO = 100
          YTDQTR_CO_AMT_raw =  100
          YTDQTR_CO_AMT =  100
          CurrQTR_CO_AMT_raw = 100
          CurrQTR_CO_AMT =  100
          lstQTR_CO_AMT_raw = 100
          lstQTR_CO_AMT = 100
          CO_CLose = 100
          AE_Ranking = 100
        
        LeadsVolume_Data = data_LeadsVolume.get_LeadsVolume()
        if len (LeadsVolume_Data) > 0 :
          LeadsVolume_Time = LeadsVolume_Data["time"].tolist()
          LeadsVolume_Projected = LeadsVolume_Data["Projected"].tolist()
          LeadsVolume_Calls = LeadsVolume_Data["Calls"].tolist()
          LeadsVolume_WebLeads = LeadsVolume_Data["WebLeads"].tolist()
          LeadsVolume_TotalCalls = LeadsVolume_Data["TotalCalls"].tolist()
        else: 
          LeadsVolume_Time = [0]
          LeadsVolume_Projected = [0]
          LeadsVolume_Calls = [0]
          LeadsVolume_WebLeads = [0]
          LeadsVolume_TotalCalls = [0]          

        ytdData_bm = ytd_data_benchmark.get_ytdData_bm (user_email)      
        if len(ytdData)>0:
          BM_YTDQTR_CO = ytdData_bm["YTDQTR_CO"] 
          BM_YTDQTR_CO_AMT_raw =  ytdData_bm["YTDQTR_CO_AMT"] 
          BM_CurrQTR_CO_AMT_raw = ytdData_bm["CurrQTR_CO_AMT"] 
          BM_lstQTR_CO_AMT_raw = ytdData_bm["lstQTR_CO_AMT"]
          BM_CO_CLose = ytdData_bm["CO Close"]          
        else:
          BM_YTDQTR_CO = 100
          BM_YTDQTR_CO_AMT_raw =  100        
          BM_CurrQTR_CO_AMT_raw =  100          
          BM_lstQTR_CO_AMT_raw = 100
          BM_CO_CLose = 100

        ytdRank = ytd_ranking.get_ytdranking(user_email)
        ytdRank_div = ytd_ranking_div.get_ytdranking_div(user_email)
        if len(ytdRank)>0:
          myRank = ytdRank["Ranking"][0]          
          myDiff = '{0:g}'.format( round(ytdRank["YCOhead"][0]) - round(ytdRank["YTDQTR_CO"][0]))
          myRankHead = '{0:g}'.format( ytdRank["Ranking"][0] - 1)          
        else:
          myRank = 1
          myDiff = "You are the Number 1"
          myRankHead = 1

        if len(ytdRank_div)>0:
          myRank_div = ytdRank_div["Ranking"][0]          
          myDiff_div = '{0:g}'.format( round(ytdRank_div["YCOhead"][0]) - round(ytdRank_div["YTDQTR_CO"][0]))
          myRankHead_div = '{0:g}'.format( ytdRank_div["Ranking"][0] - 1)          
        
        else:
          myDiff_div = "You are the Number 1"
          myRank_div = 1
          myRankHead_div = 1
 
        YTDQTR_CO_Diff = round( (YTDQTR_CO - BM_YTDQTR_CO)/ BM_YTDQTR_CO * 100 ,1) 
        YTDQTR_CO_AMT_Diff = round(  (YTDQTR_CO_AMT_raw - BM_YTDQTR_CO_AMT_raw)/ BM_YTDQTR_CO_AMT_raw * 100,1)
        CurrQTR_CO_AMT_Diff = round(  (CurrQTR_CO_AMT_raw - BM_CurrQTR_CO_AMT_raw)/ BM_CurrQTR_CO_AMT_raw * 100,1)
        lstQTR_CO_AMT_Diff = round(  (lstQTR_CO_AMT_raw - BM_lstQTR_CO_AMT_raw)/ BM_lstQTR_CO_AMT_raw * 100,1)
        CO_CLose_Diff =  round( (CO_CLose - BM_CO_CLose)/ BM_CO_CLose * 100,1)
        

        ae_pipeline_sum = AE_Pipeline_Count.get_AEPipeline_Count(user_email)

        if len(ae_pipeline_sum)>0:
          myPip = ae_pipeline_sum["Pip"][0]            
          myIP = ae_pipeline_sum["IP"][0]            
          myTotalLoans = ae_pipeline_sum["TotalPipe"][0]            
        else:
          myPip = 1
          myIP = 1
          myTotalLoans = 2

        #pipe
        aePipeline = AE_Pipeline.get_AEPipeline(user_email)         
        aePipeline_json = json.dumps(aePipeline)
        
        #pic
        img_url = 'img.jpg'

        return render(request, 'dashboard.html',
                    context={
                             'test_test':lstRunTime.day,
                             'user_email':user_email,   
                             'img_url':img_url,     
                             'isAVP':isAVP,
                             'myteam':myteam,                     
                             'YTDQTR_CO':YTDQTR_CO ,     
                             'YTDQTR_CO_AMT':YTDQTR_CO_AMT ,     
                             'CurrQTR_CO_AMT':CurrQTR_CO_AMT ,     
                             'lstQTR_CO_AMT':lstQTR_CO_AMT ,     
                             'CO_CLose':CO_CLose ,     
                             'AE_Ranking': myRank,                             
                             "myRankHead": myRankHead,
                             'AE_Ranking_div': myRank_div,
                             "myRankHead_div": myRankHead_div,                             
                             'activity_top20': activity_top20,
                             'activity_top50' : activity_top50,
                             'activity_myself': activity_myself,
                             'aePipeline_js':aePipeline,
                             'aePipeline_json':aePipeline_json,
                             'timeseries_totalLeads':timeseries_totalLeads,
                             'timeseries_AOs':timeseries_AOs,
                             'timeseries_opens':timeseries_opens,
                             'timeseries_pitches':timeseries_pitches,
                             'timeseries_tiemRange':timeseries_tiemRange,

                             'LeadsVolume_Time':LeadsVolume_Time,
                             'LeadsVolume_Projected':LeadsVolume_Projected,
                             'LeadsVolume_Calls':LeadsVolume_Calls,
                             'LeadsVolume_WebLeads':LeadsVolume_WebLeads,
                             'LeadsVolume_TotalCalls':LeadsVolume_TotalCalls,
      

                             'RouterCapture13wk_Rel':RouterCapture13wk_Rel,
                             'WebCapture13wk_Rel':WebCapture13wk_Rel,
                             'RouterClose13wk_Rel':RouterClose13wk_Rel,
                             'WebClose13wk_Rel':WebClose13wk_Rel,
                             'Open_to_pich_13wk_Rel':Open_to_pich_13wk_Rel,
                             'Pitch_to_AO_13wk_Rel':Pitch_to_AO_13wk_Rel,

                             'RouterCapture13wk_bm_Rel':RouterCapture13wk_bm_Rel,
                             'WebCapture13wk_bm_Rel':WebCapture13wk_bm_Rel,
                             'RouterClose13wk_bm_Rel':RouterClose13wk_bm_Rel,
                             'WebClose13wk_bm_Rel':WebClose13wk_bm_Rel,
                             'Open_to_pich_13wk_bm_Rel':Open_to_pich_13wk_bm_Rel,
                             'Pitch_to_AO_13wk_bm_Rel':Pitch_to_AO_13wk_bm_Rel,                             
                             'YTDQTR_CO_Diff':YTDQTR_CO_Diff,
                              'YTDQTR_CO_AMT_Diff' :YTDQTR_CO_AMT_Diff,
                              'CurrQTR_CO_AMT_Diff'  :CurrQTR_CO_AMT_Diff,
                              'lstQTR_CO_AMT_Diff'   :lstQTR_CO_AMT_Diff,
                              'CO_CLose_Diff'     :CO_CLose_Diff    ,
                              'myPip':myPip    ,
                              'myIP':myIP    ,
                              'myTotalLoans':myTotalLoans    ,
                              'myDiff':myDiff    ,
                              'RouterCapture13wk':RouterCapture13wk    ,
                              'WebCapture13wk':WebCapture13wk    ,
                              'RouterClose13wk':RouterClose13wk    ,
                              'WebClose13wk':WebClose13wk    ,
                              'Open_to_pich_13wk':Open_to_pich_13wk    ,
                              'Pitch_to_AO_13wk':Pitch_to_AO_13wk    

                            },
         ) 
    else:       
       return  redirect('accounts/login/')
    # return render(
    #     request, 
    #      'GDashboard/production/index.html',
    #      context={'num_leads_yst':num_Router_lstWk,'user_email':user_email,'form':form},
    #      ) 



def my_team_summary(request):
  img_url = 'img.jpg'
  return render(request, 'dashboard_team.html',context={'img_url':img_url,})



def equivalentRate(request):
    if request.user.is_authenticated:
                
        loanNumber = request.GET.get('loanNumber')            
        
        if loanNumber == None: loanNumber = "XXXXXXX"
        
        my_loaninfo,total_int_saved,erate1,erate2,lastPaymentYear,lastPaymentMonth = loan_info.get_LoanInfo(loanNumber)
        
        my_loaninfo_fstnm = my_loaninfo["FstNm"][0]
        my_loaninfo_lstnm = my_loaninfo["LstNm"][0]
        my_loaninfo_intrate = my_loaninfo["IntRate"][0]
        my_loaninfo_fico = my_loaninfo["FICOScore"][0]
        my_loaninfo_LoanAmt = my_loaninfo["LoanAmt"][0]
                
            
        user = request.user
        user_email = user.email.lower()
        
        isAVP = request.user.groups.filter(name__in=['avp','AVP']).exists()         
        myteam = get_myTeam.get_myTeam(user_email)
                
         
        #pic
        img_url = 'img.jpg'
        
        salesQuote = ['You will never find time for anything. If you want time you must make it. – Charles Robert Buxton',
                      'The difference between a successful person and others is not a lack of strength, not a lack of knowledge, but rather a lack of will. – Vince Lombardi',                      
                      'The difference between try and triumph is just a little umph! – Marvin Phillips',
                      'Every brand isn’t for everybody, and everybody isn’t for every brand. – Liz Lange',
                      'The most unprofitable item ever manufactured is an excuse. – John Mason',
                      'Success is the culmination of failures, mistakes, false starts, confusion, and the determination to keep going anyway. – Nick Gleason',
                      'Most people think selling is the same as talking. But the most effective salespeople know that listening is the most important part of their job.',
                      'You dont close a sale; you open a relationship if you want to build a long-term, successful enterprise. – Patricia Fripp',
                      'If you are not taking care of your customer, your competitor will. – Bob Hooey',
                      'There are no shortcuts to any place worth going. – Beverly Sills',
                      'Life’s battles don’t always go to the strongest or fastest; sooner or later those who win are those who think they can. – Richard Bach'
        ]
        return render(request, 'app_equivalentrate.html',
                    context={                        
                             'salesQuote':salesQuote,
                             'user_email':user_email,        
                             'isAVP':isAVP,
                             'myteam':myteam,      
                             
                             
                             'loanNumber':loanNumber,
                             'my_loaninfo_fstnm':my_loaninfo_fstnm,
                             'my_loaninfo_lstnm':my_loaninfo_lstnm ,
                             'my_loaninfo_intrate':my_loaninfo_intrate,
                             'my_loaninfo_fico':my_loaninfo_fico ,
                             'my_loaninfo_LoanAmt':my_loaninfo_LoanAmt ,
                             'total_int_saved':total_int_saved,
                             'erate1':erate1,
                             'erate2':erate2,
                             'lastPaymentYear':lastPaymentYear,
                             'lastPaymentMonth':lastPaymentMonth,        
                                              
                             'img_url':img_url,
                  

                            },
         ) 
    else:       
       return  redirect('accounts/login/')
    # return render(
    #     request, 
    #      'GDashboard/production/index.html',
    #      context={'num_leads_yst':num_Router_lstWk,'user_email':user_email,'form':form},
    #      ) 
      