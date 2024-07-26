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
        try:
            data = json.loads(request.body.decode('utf-8'))
            name = data['name']
            phone = data['phone']
            date = data['date']
            time = data['time']

            # Check if the time slot is already taken
            if Reservation.objects.filter(date=date, time=time).exists():
                return JsonResponse({'status': 'error', 'message': 'L\'heure est déjà prise, veuillez réserver sous une autre heure ou une autre date.'})

            # Create new reservation
            try:
                Reservation.objects.create(name=name, phone=phone, date=date, time=time)
                return JsonResponse({'status': 'success', 'message': f'Réservation effectuée à {time} le {date}.'})
            except Exception as e:
                return JsonResponse({'status': 'error', 'message': 'Échec de la réservation.'})

        except json.JSONDecodeError as e:
            return JsonResponse({'status': 'error', 'message': 'Données JSON invalides.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': 'Une erreur inattendue s\'est produite.'})

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

def coiffure(request):
	return render(request, 'dashboard/Coiffures.html')

def maquillage(request):
	return render(request, 'dashboard/maquillage.html')

def manicure(request):
	return render(request, 'dashboard/manicure.html')

def pedicure(request):
	return render(request, 'dashboard/pédicure.html')





def update_status(request, reservation_id, status):
    reservation = Reservation.objects.get(id=reservation_id)
    if status in ['Confirmé', 'Annulé']:
        reservation.status = status
        reservation.save()
    return redirect('reservations_list')


def confirmed_reservations(request):
    reservation_list = Reservation.objects.filter(status='Confirmé')
    paginator = Paginator(reservation_list, 10)  # 10 réservations par page

    page_number = request.GET.get('page')
    reservations = paginator.get_page(page_number)
    return render(request, 'adminnistrateur/confirmed_reservations.html', {'reservations': reservations})