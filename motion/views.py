
from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def membership(request):
    return render(request, 'membership.html')

def personal_trainer(request):
    return render(request, 'personal_trainer.html')

def location(request):
    return render(request, 'location.html')

def classes(request):
    return render(request, 'classes.html')

def about(request):
    return render(request, 'about.html')

