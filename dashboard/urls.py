from django.urls import path
from .views import *

app_name = "dashboard"
urlpatterns = [
    path('udis', GetUDIS.as_view(), name='udis'),
    path('dolar', GetDolar.as_view(), name='dolar'),
    path('tiie', GetTIIE.as_view(), name='tiie'),
    path('', HomeView.as_view(), name='home'),
]
