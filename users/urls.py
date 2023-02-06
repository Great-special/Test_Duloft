from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.register, name='register'),
    path('register/<str:refer_code>/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('add-profile/', views.landlordprofile, name='landlordprofile'),
    path('add-payment-details/', views.landlordpaymentdetail, name='paymentdetail'),
]