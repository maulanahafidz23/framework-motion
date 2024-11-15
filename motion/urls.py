
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('membership/', views.membership, name='membership'),
    path('personal_trainer/', views.personal_trainer, name='personal_trainer'),
    path('location/', views.location, name='location'),
    path('classes/', views.classes, name='classes'),
    path('about/', views.about, name='about'),
]
