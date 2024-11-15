# project/urls.py (Sesuaikan dengan nama proyek kamu)
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('motion.urls')),  
]
