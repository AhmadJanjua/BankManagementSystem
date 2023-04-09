from django.urls import path
from . import views

# sets the namespace
app_name = 'home'
# directs the urls from root
urlpatterns = [
    path('', views.home_view, name='home'),
]