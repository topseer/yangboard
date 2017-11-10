from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.views import login
import pyodbc 
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

from . import barcharts
from . import ytd_data
from . import AE_Pipeline


import locale
locale.setlocale( locale.LC_ALL, '' )


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
        rawdata = datatrend.datatrend(user_email)    
        timeseries_webLeads =  rawdata["WebLead"]
        timeseries_Router =rawdata["WebLead"]
        ct_activity = barcharts. get_chart_recentActivity(rawdata)

        #the top section
        ytdData = ytd_data.get_ytdData (user_email)      
        YTDQTR_CO = ytdData["YTDQTR_CO"][0].astype(int)
        YTDQTR_CO_AMT =  locale.currency (ytdData["YTDQTR_CO_AMT"][0].astype(int), grouping=True )
        YTDQTR_CO_AMT =  YTDQTR_CO_AMT [:-3]
        CurrQTR_CO_AMT = locale.currency (ytdData["CurrQTR_CO_AMT"][0].astype(int), grouping = True)
        CurrQTR_CO_AMT =  CurrQTR_CO_AMT [:-3]
        lstQTR_CO_AMT = locale.currency (ytdData["lstQTR_CO_AMT"][0].astype(int), grouping = True)
        lstQTR_CO_AMT = lstQTR_CO_AMT [:-3]
        CO_CLose = ytdData["CO Close"][0].astype(int)
        AE_Ranking = ytdData["Ranking"][0].astype(int)

        #pipe
        aePipeline = AE_Pipeline.get_AEPipeline(user_email)         
        aePipeline_json = json.dumps(aePipeline)

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
                             'AE_Ranking': AE_Ranking,
                             'timeseries_webLeads':timeseries_webLeads, 
                             'timeseries_Router':timeseries_Router ,
                             'line_chart': ct_activity,
                             'aePipeline_js':aePipeline,
                             'aePipeline_json':aePipeline_json
                            },
         ) 
    else:       
       return  redirect('accounts/login/')
    # return render(
    #     request, 
    #      'GDashboard/production/index.html',
    #      context={'num_leads_yst':num_Router_lstWk,'user_email':user_email,'form':form},
    #      ) 
 