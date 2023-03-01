from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register-account'),
    path('edit/', views.profile, name='edit-user-profile'),
]