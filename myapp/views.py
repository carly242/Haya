from django.shortcuts import render, redirect

# Create your views here.
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.utils.decorators import method_decorator


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from haya import settings
from .models import Profile, Reservation
import json
from django.core.exceptions import ValidationError
from django.utils.dateparse import parse_date, parse_time
from datetime import time as djangotime

@login_required
def reservation_page(request):
    return render(request, 'dashboard/reservation.html')


from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.views import OAuth2LoginView
from allauth.socialaccount.providers.google.views import OAuth2LoginView
from django.http import HttpResponseRedirect
from urllib.parse import urlencode


def google_login_redirect(request):
    print("Google login redirect view called")

    adapter = GoogleOAuth2Adapter(request)
    callback_url = adapter.get_callback_url(request, 'google_callback')
    authorize_url = 'https://accounts.google.com/o/oauth2/auth'  # Assurez-vous que cela est correct
    
    client_id = settings.SOCIALACCOUNT_PROVIDERS['google']['APP']['client_id']
    
    scope = 'profile email'
    response_type = 'code'

    params = {
        'client_id': client_id,
        'redirect_uri': callback_url,
        'scope': scope,
        'response_type': response_type,
    }

    url = f"{authorize_url}?{urlencode(params)}"
    print(f"Redirecting to: {url}")
    
    return HttpResponseRedirect(url)


from allauth.socialaccount.models import SocialApp, SocialLogin
from allauth.socialaccount.providers.oauth2.client import OAuth2Error, OAuth2Client
from allauth.socialaccount.helpers import complete_social_login
from requests import RequestException

"""
def google_callback(request):
    try:
        app = SocialApp.objects.get(provider='google')
    except SocialApp.DoesNotExist:
        return redirect('account_login')

    try:
        adapter = GoogleOAuth2Adapter(request)
        client = OAuth2Client(request, app.client_id, app.secret, adapter.access_token_method, adapter.access_token_url, adapter.basic_auth)
        token = client.get_access_token(request.GET.get('code'))
    except (OAuth2Error, RequestException) as e:
        return redirect('account_login')

    if token:
        login = adapter.complete_login(request, app, token, response=request.GET)
        login.token = token
        login.state = SocialLogin.state_from_request(request)
        ret = complete_social_login(request, login)

        if not ret:
            return redirect('profile')
        return ret

    return redirect('account_login')
"""



def google_callback(request):
    # Ajouter un message de débogage pour vérifier que la vue est appelée
    print("Google callback called")

    # Ajoutez une vérification de l'utilisateur après la connexion
    if request.user.is_authenticated:
        print("User is authenticated:", request.user.username)
        return redirect('test_create_profile')
    else:
        print("Pas connnecté")
        return redirect('account_login')
        

@csrf_exempt
@login_required
def reserve(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        date = request.POST.get('date')
        time = request.POST.get('time')

        # Validation des données
        if not name or not phone or not date or not time:
            messages.error(request, 'Tous les champs requis doivent être remplis.')
            return redirect('reservation_page')

        # Vérification si la date et l'heure sont valides
        try:
            date_obj = parse_date(date)
            time_obj = parse_time(time)
        except (ValueError, TypeError):
            messages.error(request, 'Date ou heure invalide.')
            return redirect('reservation_page')

        # Vérification pour les heures d'ouverture (09:00 à 18:00)
        opening_time = djangotime(9, 0)
        closing_time = djangotime(18, 0)

        if not (opening_time <= time_obj <= closing_time):
            messages.error(request, 'Les réservations ne peuvent être effectuées qu\'entre 09:00 et 18:00.')
            return redirect('reservation_page')

        # Vérification pour le jour de la semaine (pas de réservation le dimanche)
        if date_obj.weekday() == 6:
            messages.error(request, 'Les réservations ne sont pas disponibles le dimanche.')
            return redirect('reservation_page')

        # Check if the time slot is already taken
        if Reservation.objects.filter(date=date_obj, time=time_obj).exists():
            messages.error(request, 'L\'heure est déjà prise, veuillez réserver sous une autre heure ou une autre date.')
            return redirect('reservation_page')

        # Create new reservation
        try:
            Reservation.objects.create(
                user=request.user,
                name=name,
                phone=phone,
                date=date_obj,
                time=time_obj,
            )
            messages.success(request, f'Réservation effectuée à {time} le {date}.')
            return redirect('reservation_page')
        except Exception as e:
            messages.error(request, 'Échec de la réservation.')
            return redirect('reservation_page')

    return render(request, 'reservation.html')


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
    reservation = get_object_or_404(Reservation, id=reservation_id)
    if status in ['confirmed', 'cancelled']:
        reservation.status = status
        reservation.save()
    return redirect('reservations_list')


def confirmed_reservations(request):
    reservation_list = Reservation.objects.filter(status='Confirmé')
    paginator = Paginator(reservation_list, 10)  # 10 réservations par page

    page_number = request.GET.get('page')
    reservations = paginator.get_page(page_number)
    return render(request, 'adminnistrateur/confirmed_reservations.html', {'reservations': reservations})


from django.http import HttpResponse



@login_required
def profile(request):
    user = request.user
    try:
        profile = user.profile  # Accès au profil de l'utilisateur
    except Profile.DoesNotExist:
        return HttpResponse("Profile does not exist for this user.")
    
    reservations = Reservation.objects.filter(user=user)
    context = {
        'user': user,
        'profile': profile,
        'reservations': reservations,
    }
    return render(request, 'dashboard/profile.html', context)


        
def debug_view(request):
    user = request.user
    if user.is_authenticated:
        try:
            profile = Profile.objects.get(user=user)
            return HttpResponse(f"User profile exists for: {user.username}")
        except Profile.DoesNotExist:
            return HttpResponse("Profile does not exist.")
    return HttpResponse("User not authenticated.")




def test_create_profile(request):
    user = request.user
    # Crée un profil si celui-ci n'existe pas
    if not Profile.objects.filter(user=user).exists():
        Profile.objects.create(user=user)
        message = "Profil créé avec succès!"
    else:
        message = "Le profil existe déjà."

    return render(request, 'dashboard/test.html', {'message': message})


def manage_clients(request):
    profiles = Profile.objects.all()
    return render(request, 'adminnistrateur/manage_client.html', {'profiles': profiles})

def update_loyalty_points(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id)
    if request.method == 'POST':
        new_points = request.POST.get('loyalty_points')
        if new_points is not None:
            try:
                profile.loyalty_points = int(new_points)
                profile.save()
                messages.success(request, 'Points de fidélité mis à jour avec succès.')
            except ValueError:
                messages.error(request, 'Veuillez entrer un nombre valide pour les points de fidélité.')
        else:
            messages.error(request, 'Aucun point de fidélité fourni.')
    return redirect('clients')

from django.http import JsonResponse
from django.core.mail import send_mail

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Envoyer l'email
        send_mail(
            subject=f"Message de {name} via le formulaire de contact du site",
            message=message,
            from_email=email,
            recipient_list=['carlybivihou8@gmail.com'],  # Remplacez par votre adresse e-mail
            fail_silently=False,
        )

        return JsonResponse({'success': True, 'message': 'Votre message a été envoyé avec succès.'})

    return JsonResponse({'success': False, 'message': 'Méthode non autorisée.'})
