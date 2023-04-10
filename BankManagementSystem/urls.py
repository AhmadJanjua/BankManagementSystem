from django.contrib import admin
from django.contrib.auth.views import LoginView
from django.urls import path, include


# url mapping; input url -> page
urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('', include('home.urls')),
    path('account/', include("account.urls")),
    path('customer/', include("customer.urls")),
    path('department/', include("department.urls")),
    path('employee/', include('employee.urls')),
    path('loan/', include("loan.urls")),
    path('transaction/', include("transaction.urls")),
]
