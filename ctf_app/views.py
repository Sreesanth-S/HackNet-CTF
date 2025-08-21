from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods, require_POST
from django.middleware.csrf import get_token
from django.contrib import messages
from django.utils import timezone
from .models import CTFUser, FlagSubmission, Challenge
import json

def get_client_ip(request):
    """Get client's IP address."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@require_http_methods(["GET"])
def login_view(request):
    """Render the login page and set initial cookie."""
    # Clear any existing authentication
    request.session.pop('hacknet_authenticated', None)
    
    context = {
        'csrf_token': get_token(request)
    }
    
    # Create response with the login page
    response = render(request, 'ctf_app/index.html', context)
    
    # Set the cookie automatically when the page loads
    # Check if cookie doesn't already exist to avoid overwriting
    if not request.COOKIES.get('42find_me0'):
        response.set_cookie(
            '42find_me0', 
            'socialmedia', 
            max_age=86400,  # 1 day
            httponly=False,  # Allow JavaScript access if needed
            secure=False,    # Set to True in production with HTTPS
            samesite='Lax'   # CSRF protection
        )
    
    return response

@csrf_protect
@require_POST
def authenticate_user(request):
    """Handle user authentication."""
    try:
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        
        # Check credentials (same as original)
        if username == "42find_me0" and password == "elumban@99":
            # Set session authentication
            request.session['hacknet_authenticated'] = True
            request.session['username'] = username
            request.session.set_expiry(3600)  # 1 hour
            
            # Store CTF user in database
            ctf_user, created = CTFUser.objects.get_or_create(
                session_key=request.session.session_key,
                defaults={
                    'username': username,
                    'is_authenticated': True,
                }
            )
            if not created:
                ctf_user.is_authenticated = True
                ctf_user.username = username
                ctf_user.save()
            
            response_data = {
                'success': True,
                'message': 'Authentication successful',
                'redirect_url': '/home/'
            }
            response = JsonResponse(response_data)
            
            # Ensure cookie is set after authentication as well
            if not request.COOKIES.get('42find_me0'):
                response.set_cookie('42find_me0', 'socialmedia', max_age=86400)
            
            return response
        else:
            return JsonResponse({
                'success': False,
                'message': 'Invalid credentials'
            }, status=401)
            
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': 'Authentication error'
        }, status=500)

def check_authentication(request):
    """Check if user is authenticated."""
    return request.session.get('hacknet_authenticated', False)

@require_http_methods(["GET"])
def home_view(request):
    """Render the home page with flag submission form."""
    if not check_authentication(request):
        return HttpResponseForbidden("Access Denied! Please login first.")
    
    context = {
        'csrf_token': get_token(request),
        'username': request.session.get('username', 'Anonymous'),
        'cookie_value': request.COOKIES.get('42find_me0', 'Not set')  # Show cookie value for debugging
    }
    
    response = render(request, 'ctf_app/home.html', context)
    
    # Ensure cookie is set on home page as well
    if not request.COOKIES.get('42find_me0'):
        response.set_cookie('42find_me0', 'socialmedia', max_age=86400)
    
    return response

@csrf_protect
@require_POST
def submit_flag(request):
    """Handle flag submission."""
    if not check_authentication(request):
        return JsonResponse({
            'success': False,
            'message': 'Not authenticated'
        }, status=403)
    
    try:
        submitted_flag = request.POST.get('flag', '').strip().lower()
        correct_flag = "12022007_codaninsurance"
        
        # Get or create CTF user
        try:
            ctf_user = CTFUser.objects.get(session_key=request.session.session_key)
        except CTFUser.DoesNotExist:
            ctf_user = None
        
        # Check if flag is correct
        is_correct = (submitted_flag == correct_flag.lower())
        
        # Store submission in database
        submission = FlagSubmission.objects.create(
            ctf_user=ctf_user,
            session_key=request.session.session_key,
            submitted_flag=submitted_flag,
            is_correct=is_correct,
            ip_address=get_client_ip(request)
        )
        
        if is_correct:
            # Update session with success
            request.session['flag_captured'] = True
            request.session['score'] = request.session.get('score', 0) + 150
            
            return JsonResponse({
                'success': True,
                'message': 'Flag captured successfully!',
                'correct': True,
                'score': request.session.get('score', 150)
            })
        else:
            return JsonResponse({
                'success': False,
                'message': 'Invalid flag! Try again.',
                'correct': False,
                'hint': 'Examine the image more carefully...'
            })
            
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': 'Submission error'
        }, status=500)

@csrf_protect
@require_POST
def set_cookie_view(request):
    """Set cookie for the CTF challenge (manual endpoint)."""
    if not check_authentication(request):
        return JsonResponse({
            'success': False,
            'message': 'Not authenticated'
        }, status=403)
    
    response = JsonResponse({'success': True, 'message': 'Cookie set manually'})
    response.set_cookie('42find_me0', 'socialmedia', max_age=86400)  # 1 day
    return response
