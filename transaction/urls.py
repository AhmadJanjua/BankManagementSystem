from django.urls import path
from .views import *

# sets the namespace
app_name = 'transaction'
# directs the urls from root
urlpatterns = [
    path('perform/<str:cid>/<int:account_id>', perform_trans, name='perform'),
]