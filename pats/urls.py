from django.urls import path
from . import views

appname = 'pats'

urlpatterns = [
    path('', views.index, name='index'),
    path('map/', views.mapPage, name='mapPage'),
    #path('get/ajax/mapData', views.mapRequest, name='mapRequest'),
    path('<str:account>/', views.account_query, name='account_query'),
    path('<str:account>/valuation/', views.valuation, name='valuation'),
   
    
]