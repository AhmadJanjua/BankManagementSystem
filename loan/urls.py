from django.urls import path
from .views import create_loan, view_modify_loan,delete_loan

# sets the namespace
app_name = 'loan'
# directs the urls from root
urlpatterns = [
    path('create_loan/<str:cid>', create_loan , name='create_loan'),
    path('view_modify_loan/<int:loanNo>',view_modify_loan,name='view_modify_loan'),
    path('delete_loan/<int:loanNo>',delete_loan,name='delete_loan'),

]