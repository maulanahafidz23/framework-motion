# project/urls.py (Sesuaikan dengan nama proyek kamu)
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
<<<<<<< HEAD
    path('', include('motion.urls')),
=======
    path('', include('motion.urls')),  
>>>>>>> 3b6734edb90d6e447b71ac8e82b767e9d66e1208
]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)