from django.shortcuts import render

from pages.models import Team


# Create your views here.
def home(request):
    team = Team.objects.all()
    return render(request, 'pages/home.html', {'team': team})

def about(request):
    team = Team.objects.all()
    return render(request, 'pages/about.html', {'team': team})

def services(request):
    return render(request, 'pages/services.html')

def contact(request):
    return render(request, 'pages/contact.html')

