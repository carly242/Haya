from django.shortcuts import render, redirect

# Create your views here.
from django.contrib import messages


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Reservation
import json

def reservation_page(request):
    return render(request, 'dashboard/reservation.html')

@csrf_exempt
def reserve(request):
    if request.method == 'POST':
        name = request.POST['name']
        phone = request.POST['phone']
        time = request.POST['time']
        date = request.POST['date']

        # Check if the time slot is already taken
        if Reservation.objects.filter(date=date, time=time).exists():
            messages.error(request, 'L\'heure est déjà prise, veuillez réserver sous une autre heure ou une autre date.')
            return redirect('reservation_page')  # Assurez-vous que cette vue renvoie à votre page de réservation

        # Create new reservation
        try:
            Reservation.objects.create(name=name, phone=phone, date=date, time=time)
            messages.success(request, f'Réservation effectuée à {time} le {date}.')
        except Exception as e:
            messages.error(request, 'Échec de la réservation.')
            return redirect('reservation_page')


    return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée.'})





def home(request):
	return render(request, 'dashboard/home.html')

from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator

def reservations_list(request):
    reservations_list = Reservation.objects.all()
    paginator = Paginator(reservations_list, 10)  # Afficher 10 réservations par page
    page_number = request.GET.get('page')
    reservations = paginator.get_page(page_number)
    
    return render(request, 'adminnistrateur/admin.html', {'reservations': reservations, 'paginator': paginator})

def delete_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    reservation.delete()
    return redirect('reservations_list')