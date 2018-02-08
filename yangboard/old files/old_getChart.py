from jchart import Chart
from jchart.config import Axes, DataSet, rgba, Tick


class BarChart(Chart):
    chart_type = 'bar'
    scales = {
        'xAxes': [Axes(display=True)],
    }
    
    title = {
        'text':'yang',
        'display':'True',
    }
    
    options = {
        'maintainAspectRatio': True
    }
    
        
    def get_labels(self, **kwargs):
        return ["January", "February", "March", "April",
                "May", "June", "July"]

    def get_datasets(self, **kwargs):
        data = [10, 15, 29, 30, 5, 10, 22]
        colors = [
            rgba(255, 99, 132, 0.2) 
        ]
        

        return [DataSet(label='Bar Chart',
                        data=data,
                    #    height = 50,
                        borderWidth=1,
                        backgroundColor=colors,
                        borderColor=colors)               
        ]

class RadarChart(Chart):
    chart_type = 'radar'
    responsive = True
    def get_labels(self):
        return ["Router Capture","Web-Capture", "Open-Pitch", "Pitch-AO", "Router-Close","Web-Close"]

    def get_datasets(self, **kwargs):
        return [DataSet(label="My First dataset",
                        color=(179, 181, 198),                        
                        data=[65, 59, 90, 81, 56, 55]),
                DataSet(label="My Second dataset",
                        color=(255, 99, 132),
                        data=[28, 48, 40, 19, 96, 27])
               ]
   
class getEfficiencyRadar(Chart):
    chart_type = 'radar'       
    responsive = False
#    scales = {        
#        'yAxes': [Axes(
#                       ticks=Tick(minRotation=0, fontColor='#d02828')
#                       )],                                                      
#      }  

    scales =  {
                'yAxes': [{
                    'ticks': {
                        'max':500,
                        'min':100
                    }
                }]
    } 
     
        
    def __init__(self, queryResult):
        #timeseries_data = datatrend.datatrend(user_email)            
        super().__init__()
        RouterCapture13wk = queryResult["Router Capture 13wk"][0]
        WebCapture13wk = queryResult["Web Capture 13wk"][0]
        RouterClose13wk = queryResult["Router Close 13wk"][0]
        WebClose13wk = queryResult["Web Close 13wk"][0]
        Open_to_pich_13wk = queryResult["Open-Pitch 13wk"][0]
        Pitch_to_AO_13wk = queryResult["Pitch-AO 13wk"][0]
        RouterCapture13wk_bm = queryResult["Router Capture BM"][0]
        WebCapture13wk_bm = queryResult["Web Capture BM"][0]
        RouterClose13wk_bm = queryResult["Router Close BM"][0]
        WebClose13wk_bm = queryResult["Web Close BM"][0]
        Open_to_pich_13wk_bm = queryResult["Open-Pitch BM"][0]
        Pitch_to_AO_13wk_bm = queryResult["Pitch-AO BM"][0]
        
        self.RouterCapture13wk_Rel= RouterCapture13wk / RouterCapture13wk_bm * 100
        self.WebCapture13wk_Rel= WebCapture13wk / WebCapture13wk_bm * 100
        self.RouterClose13wk_Rel= RouterClose13wk / RouterClose13wk_bm * 100
        self.WebClose13wk_Rel= WebClose13wk / WebClose13wk_bm * 100
        self.Open_to_pich_13wk_Rel= Open_to_pich_13wk / Open_to_pich_13wk_bm * 100
        self.Pitch_to_AO_13wk_Rel= Pitch_to_AO_13wk / Pitch_to_AO_13wk_bm * 100
        
        
        self.RouterCapture13wk_bm_Rel = 100
        self.WebCapture13wk_bm_Rel = 100
        self.RouterClose13wk_bm_Rel = 100
        self.WebClose13wk_bm_Rel = 100
        self.Open_to_pich_13wk_bm_Rel = 100
        self.Pitch_to_AO_13wk_bm_Rel = 100
        
  
         
    def get_labels(self):
        return ["Router Capture","Web-Capture", "Open-Pitch", "Pitch-AO", "Router-Close","Web-Close"]

    def get_datasets(self, **kwargs):
        return [DataSet(label="My First dataset",
                        color=(179, 181, 198),                        
                        data=[self.RouterCapture13wk_bm_Rel, self.WebCapture13wk_bm_Rel, self.RouterClose13wk_bm_Rel, self.WebClose13wk_bm_Rel, self.Open_to_pich_13wk_bm_Rel, self.Pitch_to_AO_13wk_bm_Rel],
                        ),
                
      DataSet(label="My Second dataset",
                        color=(255, 99, 132),
                        data=[self.RouterCapture13wk_Rel,self. WebCapture13wk_Rel, self.RouterClose13wk_Rel, self.WebClose13wk_Rel, self.Open_to_pich_13wk_Rel, self.Pitch_to_AO_13wk_Rel],                        
                        )
               ]
        
        
        

class get_chart_recentActivity(Chart):
    chart_type = 'bar'    
    responsive = True
    scales = {
        'xAxes': [Axes(display=True)],
    }    
    options = {
        'maintainAspectRatio': True,
        
    }
#   title = {'text':'yang', 'display':'False',  }        

    def __init__(self, rawdata):
        #timeseries_data = datatrend.datatrend(user_email)            
        super().__init__()
        self.timeseries_data = rawdata
        self.timeseries_totalLeads = (rawdata["WebLead"] +rawdata["RouterCall"] + rawdata["TransferIn"] - rawdata["TransferOut"]).tolist()
        self.timeseries_AOs = rawdata["AO"].tolist()
        self.timeseries_opens = rawdata["Capture"].tolist()
        self.timeseries_pitches = rawdata["Pitch"].tolist()        
        self.timeseries_tiemRange = rawdata["StartOfWeek"] .tolist()

    def get_labels(self, **kwargs):
        return self.timeseries_tiemRange
        #return ["January", "February", "March", "April","May", "June", "July"]
    def get_datasets(self, **kwargs):
        total_Leads = self.timeseries_totalLeads
        total_Opens = self.timeseries_opens
        total_Pitches = self.timeseries_pitches
        total_AOs = self.timeseries_AOs
        #data = [10, 15, 29, 30, 5, 10, 22]
        
        colors = [rgba(0, 76, 112, 0.2) ]
        color1 = rgba(0, 76, 112, 0.8) 
        color2 = rgba(0, 147, 209, 0.8)
        color3 = rgba(242, 99, 95, 0.8) 
        color4 = rgba(244, 208, 12, 0.8) 
        
        return [DataSet(label='Leads',
                        data=total_Leads,                    
                        borderWidth=1,
                        backgroundColor=color1,
                        borderColor=color1),
                DataSet(label='Opens',
                        data=total_Opens,                    
                        borderWidth=1,
                        backgroundColor=color2,
                        borderColor=color2),             
                DataSet(label='Pitches',
                        data=total_Pitches,                    
                        borderWidth=1,
                        backgroundColor=color3,
                        borderColor=color3),                                                      
                DataSet(label='AOs',
                        data=total_AOs,                    
                        borderWidth=1,
                        backgroundColor=color4,
                        borderColor=color4),    
        ]


