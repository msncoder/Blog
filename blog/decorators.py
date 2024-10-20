from functools import wraps
from django.http import JsonResponse
from django.conf import settings
from django.shortcuts import redirect
from urllib.parse import urlencode

def login_required_custom(view_function):
    @wraps(view_function)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                # For AJAX requests, return a JSON response indicating not authenticated
                return JsonResponse({'error': 'You need to log in to like this post.'}, status=403)
            else:
                # For regular requests, redirect to the login page
                path = request.get_full_path()
                login_url = f"{settings.LOGIN_URL}?{urlencode({'next': path})}"
                return redirect(login_url)
        return view_function(request, *args, **kwargs)
    return wrapper
