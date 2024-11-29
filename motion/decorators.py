from django.http import HttpResponseForbidden
from django.contrib import messages
from django.shortcuts import redirect

def admin_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.groups.filter(name='Admin').exists():
            return view_func(request, *args, **kwargs)
        messages.error(request, 'Anda tidak memiliki izin untuk mengakses halaman ini.')
        return redirect('login')
    return _wrapped_view

