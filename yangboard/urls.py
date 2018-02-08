from django.conf.urls import url
from . import views


# Create your tests here.

urlpatterns = [    
    url(r'^app_equivalentrate/(?P<loanNumber>\w+)/$', views.equivalentRate, name='equivalentRate'),
    url(r'^app_equivalentrate', views.equivalentRate, name='equivalentRate'),
    url(r'^$', views.dashboard, name='dashboard'),
    url(r'^dashboard/(?P<loanNumber>\w+)/$', views.dashboard, name='dashboard'),
    url(r'^dashboard/myteam/(?P<team_member_email>\w+|[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/$', views.my_team_member, name='my_team_member'),
    url(r'^dashboard/teamDashboard/', views.my_team_summary, name='my_team_summary'),
    url(r'^myPipeline/', views.myPipeline, name='myPipeline'),
    url(r'^/myPipeline/', views.myPipeline, name='myPipeline')
    ]

 
 
#urlpatterns += [   
#    url(r'^dashboard/dateRange/$', views.dashboard, name='dashboard'),
#]
