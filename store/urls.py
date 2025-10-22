from django.urls import path
from . import views

app_name = 'store' 

urlpatterns = [
    path('', views.home, name='home'),
    path('cars/', views.browse_cars, name='cars'),
    path('cars/<int:car_id>/', views.car_detail, name='car_detail'),
    path('contact/', views.contact, name='contact'),
]
