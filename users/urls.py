from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.register, name='register'),
    path('register/<str:refer_code>/', views.register, name='register'),
    path('update/<str:pk>/', views.update_view, name='edit-profile'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('add-profile/', views.landlordprofile, name='landlordprofile'),
    path('update-landlord-profile/<str:pk>/', views.update_landlord_profile, name='edit-landlord-profile'),
    path('add-payment-details/', views.landlordpaymentdetail, name='paymentdetail'),
    path('', views.userdetailsView, name='userprofile'),
    path('my-properties/', views.get_building_for_tenant, name='my-properties'),
    
    path('dashboard/', views.landlordDashboardView, name='landlord-dashboard'),
    path('dashboard/my-properties/', views.get_buildings_by_landlord, name='my-properties-dashboard'),
]