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
         
         path('profile/', profile, name='profile'),
         path('contact/', contact, name='contact'),

         
         path('accounts/google/login/', google_login_redirect, name='google-login-redirect'),
         path('accounts/google/login/callback/', google_callback, name='google_callback'),

        path('debug/', debug_view, name='debug_view'),
        
        path('test-create-profile/', test_create_profile, name='test_create_profile'),
        
        path('clients/', manage_clients, name='clients'),
        path('/profiles/update/<int:profile_id>/', update_loyalty_points, name='update_loyalty_points'),






]
