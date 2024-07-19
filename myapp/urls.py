from django.urls import path, include
from .views import *



urlpatterns = [
    
         path('', home, name='home'),
         path('reserve/', reservation_page, name='reservation_page'),
         path('api/reserve', reserve, name='reserve'),
         path('reservations/', reservations_list, name='reservations_list'),
         path('reservations/delete/<int:reservation_id>/', delete_reservation, name='delete_reservation'),



]
