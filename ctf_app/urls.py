"""
URL configuration for ctf_app.
"""
from django.urls import path
from . import views

app_name = 'ctf_app'

urlpatterns = [
    path('', views.login_view, name='login'),
    path('home/', views.home_view, name='home'),
    path('authenticate/', views.authenticate_user, name='authenticate'),
    path('submit_flag/', views.submit_flag, name='submit_flag'),
    path('set_cookie/', views.set_cookie_view, name='set_cookie'),
]