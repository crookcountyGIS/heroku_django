from django.urls import path
from . import views

appname = 'pats'

urlpatterns = [
    path('', views.index, name='index'),
    path('base/', views.base, name='base'),
    path('map/', views.mapPage, name='mapPage'),
    path('<str:account>/', views.account_query, name='account_query'),
    path('<str:account>/valuation/', views.valuation, name='valuation'),
    path('search/<str:value>/', views.tableSearchResults, name='tableSearchResults'),
   
]