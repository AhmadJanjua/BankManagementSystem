from django.urls import path
from . import views

# sets the namespace
app_name = 'transaction'
# directs the urls from root
urlpatterns = [
    path('transactions/', views.teller_transactions, name='teller_transactions'),
]