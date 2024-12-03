from django.http  import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse('users', args=[request.user.id]))
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group=request.user.groups.all()[0].name
            if group in allowed_roles:
            # print('Working:', allowed_roles)
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('You are not authorised to view this page!')
        return wrapper_func
    return decorator

def admin_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group=request.user.groups.all()[0].name

        if group == 'just user':
        # print('Working:', allowed_roles)
            return redirect(reverse('users', args=[request.user.id]))
        
        if group == 'admin':
            return view_func(request, *args, **kwargs)
    return wrapper_func