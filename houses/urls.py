from django.urls import path

from . import views




urlpatterns = [
    path('', views.index_view, name = 'index'), 
    path('accommodation/', views.HouseModelListView.as_view(), name = 'houses'), 
    path('accommodation/search/', views.lookupform_view, name = 'lookup'),
    path('accommodation/search/ <str:keyword>/', views.lookup_accommodation, name = 'keyword-lookup'), 
    path('accommodation/property-search/ <str:keyword>/', views.lookup_property_by_type, name = 'property-lookup'), 
    path('accommodation/add/house/', views.house_create_view, name = 'add-house'), 
    path('accommodation/update/house/<int:id>/', views.house_update_view, name = 'edit-house'), 
    path('accommodation/add/flat/', views.flat_create_view, name = 'add-flat'), 
    path('accommodation/update/flat/<int:id>/', views.flat_update_view, name = 'edit-flat'), 
    path('accommodation/add/space/', views.space_create_view, name = 'add-space'), 
    path('accommodation/update/space/<int:id>/', views.space_update_view, name = 'edit-space'), 
    path('accommodation/ <int:pk>/', views.HouseModelDetailView.as_view(), name = "house-detail"), 
    path('accommodation/flat/<int:pk>/', views.FlatModelDetailView.as_view(), name = 'flat-detail'), 
    path('accommodation/<int:pk>/flats/', views.get_flats_by_building, name = "flats-by-building"),
    
    path('ajax/load-states/', views.load_states, name = 'ajax_load_states'), 
    path('ajax/load-cities/', views.load_cities, name = 'ajax_load_cities'), 
]
