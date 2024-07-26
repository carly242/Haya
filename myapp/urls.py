from django.urls import path, include
from .views import *



urlpatterns = [
    
         path('', home, name='home'),
         path('reserve/', reservation_page, name='reservation_page'),
         path('api/reserve', reserve, name='reserve'),
         path('reservations/', reservations_list, name='reservations_list'),
         path('reservations/delete/<int:reservation_id>/', delete_reservation, name='delete_reservation'),
         path('update_status/<int:reservation_id>/<str:status>/', update_status, name='update_status'),
             path('confirmed-reservations/', confirmed_reservations, name='confirmed_reservations'),


         
         path('coiffures/', coiffure, name='coiffure'),
         path('maquillage/', maquillage, name='maquillage'),
         path('manicure/', manicure, name='manicure'),
         path('pedicure/', pedicure, name='pedicure'),




]
