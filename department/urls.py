from django.urls import path
from .views import *

# sets the namespace
app_name = 'department'
# directs the urls from root
urlpatterns = [
    path('create/', create_department, name='create_department'),
]