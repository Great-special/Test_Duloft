from django.urls import path

from . import views




urlpatterns = [
    path('accommodation/', views.HouseModelListView.as_view(), name='houses'),
    path('accommodation/search/', views.lookupformView, name='lookup'),
    path('accommodation/add/house/', views.houseCreateView, name='add-house'),
    path('accommodation/add/house/<int:id>/', views.houseUpdateView, name='edit-house'),
    path('accommodation/add/flat/', views.flatCreateView, name='add-flat'),
    path('accommodation/add/flat/<int:id>/', views.flatUpdateView, name='add-flat'),
    path('accommodation/<int:pk>/', views.HouseModelDetailView.as_view(), name="house-detail"),
    path('accommodation/flat/<int:pk>/', views.FlatModelDetailView.as_view(), name='flat-detail'),
    path('accommodation/<int:pk>/flats/', views.get_flatsByBuilding, name="flats-by-building"),
    
    path('ajax/load-states/', views.load_states, name='ajax_load_states'),
    path('ajax/load-cities/', views.load_cities, name='ajax_load_cities'),
]
