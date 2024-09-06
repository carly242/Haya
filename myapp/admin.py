# admin.py
from django.contrib import admin
from .models import Reservation, Profile

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'date', 'time')
    list_filter = ('date', 'time')
    search_fields = ('name', 'phone')


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'loyalty_points')
    list_filter = ('loyalty_points',)
    search_fields = ('user__username', 'phone')
    fields = ('user', 'phone', 'loyalty_points')
    readonly_fields = ('loyalty_points',)

# Register the Profile model with the ProfileAdmin class
