from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect

from .forms import UpdateUserForm, UpdateUserProfileForm

User = get_user_model()

@csrf_protect
def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        is_error = False
        if len(password1) == 0 or password1 != password2:
            is_error = True
            messages.error(request, "Password do not match or were not entered.")
        if len(username) == 0 or User.objects.filter(username=username).exists():
            is_error = True
            messages.error(request, "Username already taken or was not entered.")
        if len(email) == 0 or User.objects.filter(email=email).exists():
            is_error = True
            messages.error(request, "User with this email already exists, or email was not entered.")
        if not is_error:            
            try:
                User.objects.create_user(username=username, email=email, password=password1)
            except Exception as e:
                is_error = True
                messages.error(request, str(e))
        if not is_error:
            messages.success(request, f'user {username} has been succesfully registered. You can log in now.')
            return redirect(reverse_lazy('login'))
    return render(request, 'user_profile/register.html')

@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateUserProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='edit-user-profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateUserProfileForm(instance=request.user.profile)

    return render(request, 'user_profile/profile.html', {'user_form': user_form, 'profile_form': profile_form})