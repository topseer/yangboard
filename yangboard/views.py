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
from . import numOfLeads
from . import datatrend
from django.http import JsonResponse
from . import forms
from .forms import NameForm
from .forms import PeriodFilter

from random import randint
from django.views.generic import TemplateView
from jchart import Chart
from random import randint
from datetime import datetime, timedelta

from jchart import Chart
from jchart.config import Axes, DataSet, rgba
from django.contrib.staticfiles.templatetags.staticfiles import static

from . import getChart
from . import ytd_data
from . import AE_Pipeline
from . import getEfficiency
from . import ytd_data_benchmark
from . import ytd_ranking
from . import ytd_ranking_div
from . import AE_Pipeline_Count
import locale
locale.setlocale( locale.LC_ALL, '' )
from . import data_LeadsVolume

import json
# ...



def dashboard(request):
    if request.user.is_authenticated():
        user = request.user
        user_email = user.email
        from_date = date.today()
        to_date = date.today()
        
        if request.method == 'POST':
            form = PeriodFilter(request.POST)
            if form.is_valid():
                (from_date, to_date) = form.cleaned_data['Range']    
        else:
            form = PeriodFilter(initial={'range': (date.today(), date.today())})

        #leads
        num_Router_lstWk= numOfLeads.numOfRouterCalls(from_date.strftime('%Y-%m-%d'), to_date.strftime('%Y-%m-%d'),user_email)
        num_Web_lstWk= numOfLeads.numOfWebLeads(from_date.strftime('%Y-%m-%d'), to_date.strftime('%Y-%m-%d'),user_email)
        numOfAOs= numOfLeads.numOfAOs(from_date.strftime('%Y-%m-%d'), to_date.strftime('%Y-%m-%d'),user_email)
        numOfIPs= numOfLeads.numOfIPs(from_date.strftime('%Y-%m-%d'), to_date.strftime('%Y-%m-%d'),user_email)
        numOfFunds= numOfLeads.numOfFunds(from_date.strftime('%Y-%m-%d'), to_date.strftime('%Y-%m-%d'),user_email)
        numOfPitch= numOfLeads.numOfPitch(from_date.strftime('%Y-%m-%d'), to_date.strftime('%Y-%m-%d'),user_email)
        
        
        #charts of activity
        activity_rawdata = datatrend.datatrend(user_email)        
        #old method
        #ct_activity = getChart. get_chart_recentActivity(activity_rawdata)
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
        #old way
        #ct_efficiency = getChart. getEfficiencyRadar(efficiency_rawdata)                
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
                    context={'num_router_leads':num_Router_lstWk,'user_email':user_email,'form':form,
                             'num_web_leads':num_Web_lstWk,
                             'numOfAOs':numOfAOs,
                             'numOfIPs':numOfIPs,
                             'numOfFunds':numOfFunds,
                             'numOfPitch':numOfPitch ,                 
                             'YTDQTR_CO':YTDQTR_CO ,     
                             'YTDQTR_CO_AMT':YTDQTR_CO_AMT ,     
                             'CurrQTR_CO_AMT':CurrQTR_CO_AMT ,     
                             'lstQTR_CO_AMT':lstQTR_CO_AMT ,     
                             'CO_CLose':CO_CLose ,     
                             'AE_Ranking': myRank,                             
                             "myRankHead": myRankHead,
                             'AE_Ranking_div': myRank_div,
                             "myRankHead_div": myRankHead_div,                             
                             #'line_chart': ct_activity,
                             #'radar_efficiency': ct_efficiency,
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
   