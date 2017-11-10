from jchart import Chart
from jchart.config import Axes, DataSet, rgba


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
        'maintainAspectRatio': False
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



class get_chart_recentActivity(Chart):
    chart_type = 'bar'    
    scales = {
        'xAxes': [Axes(display=True)],
    }
       
    options = {
        'maintainAspectRatio': False
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


