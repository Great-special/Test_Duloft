from django.urls import path
from .views import make_payment, initiate_payment, verify_payment, initiate_payment_maintest



urlpatterns = [
    path('', initiate_payment, name='initiate-payment'),
    path('<str:house_id>/<str:flat_id>/', initiate_payment_maintest, name='initiate-payment'),
    path('<str:ref>/', verify_payment, name="verify-payment")
]