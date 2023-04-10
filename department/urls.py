from django.urls import path
from .views import *

# sets the namespace
app_name = 'department'
# directs the urls from root
urlpatterns = [
    path('create/', create_department, name='create_department'),
    path('delete/<int:dept_id>/', delete, name='delete'),
    path('edit/<int:dept_id>/', edit, name='edit'),
    path('search/', search_dept, name='search'),
    path('home/', display_dept, name='home'),
]