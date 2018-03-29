from django.conf.urls import url
from . import views


# Create your tests here.

urlpatterns = [        
  
    url(r'^homepage/', views.HomePage, name='HomePage'),        
    url(r'myPipeline/myteam/(?P<team_member_email>\w+|[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/$', views.my_team_member_pipeline, name='my_team_member_pipeline'),        
    url(r'^dashboard/myteam/(?P<team_member_email>\w+|[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/$', views.my_team_member, name='my_team_member'),        

    url(r'^dashboard/', views.dashboard, name='dashboard'),           
    url(r'myPipeline/$', views.myPipeline, name='myPipeline'),    
     url(r'myTeamPipeline/$', views.my_team_total_pipeline, name='my_team_total_pipeline'),    
    url(r'myTeamProspect/$', views.my_team_total_pipeline, name='my_team_total_pipeline'),    
    url(r'^$', views.HomePage, name='HomePage'),    
    ]

 
 
#urlpatterns += [   
#    url(r'^dashboard/dateRange/$', views.dashboard, name='dashboard'),
#]
