import os
import requests
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from concert.forms import LoginForm
from concert.models import Concert, ConcertAttending

def index(request):
    return render(request, 'index.html')

def signup(request):
    form = UserCreationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        login(request, form.save())
        return redirect('index')
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    form = LoginForm(request=request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        login(request, form.get_user())
        return redirect('index')
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('index')

def service_data(request, setting, default, endpoint):
    try:
        response = requests.get(os.environ.get(setting, default).rstrip('/') + endpoint, timeout=5)
        response.raise_for_status()
        return response.json()
    except (requests.RequestException, ValueError):
        messages.error(request, 'The media service is currently unavailable. Please try again later.')
        return []

def songs(request):
    data = service_data(request, 'SONGS_SERVICE_URL', 'http://127.0.0.1:8080', '/song')
    if isinstance(data, dict):
        data = data.get('songs', [])
    return render(request, 'songs.html', {'songs': data})

def photos(request):
    data = service_data(request, 'PICTURES_SERVICE_URL', 'http://127.0.0.1:8081', '/picture')
    page = Paginator(data, 1).get_page(request.GET.get('page', 1))
    return render(request, 'photos.html', {'photos': page, 'page': page})

def concerts(request):
    rows = []
    for concert in Concert.objects.order_by('date'):
        attendance = concert.attendee.filter(user=request.user).first() if request.user.is_authenticated else None
        rows.append({'concert': concert, 'status': attendance.attending if attendance else '-'})
    return render(request, 'concerts.html', {'concerts': rows})

def concert_detail(request, id):
    if not request.user.is_authenticated:
        return redirect('login')
    concert = get_object_or_404(Concert, pk=id)
    attendance = concert.attendee.filter(user=request.user).first()
    return render(request, 'concert_detail.html', {'concert_details': concert, 'status': attendance.attending if attendance else '-', 'attending_choices': ConcertAttending.AttendingChoices.choices})

@require_POST
def concert_attendee(request):
    if not request.user.is_authenticated:
        return redirect('login')
    concert = get_object_or_404(Concert, pk=request.POST.get('concert_id'))
    choice = request.POST.get('attendee_choice')
    if choice not in ConcertAttending.AttendingChoices.values:
        return redirect('concert_detail', id=concert.id)
    ConcertAttending.objects.update_or_create(concert=concert, user=request.user, defaults={'attending': choice})
    return redirect('concerts')
