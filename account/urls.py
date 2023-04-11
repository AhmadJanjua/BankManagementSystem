from django.urls import path
from .views import *

# sets the namespace
app_name = 'account'
# directs the urls from root
urlpatterns = [
    path('savings/create/<str:cid>', create_savings, name='create_savings'),
    path('chequing/create/<str:cid>', create_chequing, name='create_chequing'),
]