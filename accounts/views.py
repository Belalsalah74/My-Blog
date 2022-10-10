from django.contrib.messages import add_message, SUCCESS
from django.urls import reverse
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import login, logout
from django.contrib.auth.models import User

from .forms import ProfileUpdate_CreateForm, UserUpdateForm, UserSignUpForm, PassChangeForm, UserLoginForm



def user_register(request):
    form = UserSignUpForm(request.POST or None)
    profile_form = ProfileUpdate_CreateForm(
        request.POST or None, request.FILES or None)
    context = {'form': form, 'profile_form': profile_form}
    print(request.GET)
    if form.is_valid() and profile_form.is_valid():
        user = form.save()
        profile = profile_form.save(commit=False)
        profile.user = user
        profile.save()
        login(request, user)
        if 'next' in request.POST:
            return redirect(request.POST['next'])
        return redirect('home')
    return render(request, 'accounts/register.html', context)


def user_login(request):
    form = UserLoginForm(data=request.POST or None)
    context = {'form': form}
    if form.is_valid():
        user = form.get_user()
        login(request, user)
        if 'next' in request.GET:
            return redirect(request.GET['next'])
        return redirect('home')
    return render(request, 'accounts/login.html', context)


def user_logout(request):
    if request.POST:
        logout(request)
        return redirect('accounts:login')

def profile_view(request, id):
    user = get_object_or_404(User, id=id)
    context = {'profile': user.profile}
    return render(request, 'accounts/profile.html', context)


def udpate_profile(request, id):
    user = get_object_or_404(User, id=id)
    if request.user == user or request.user.is_staff:    
        profile = user.profile
        user_form = UserUpdateForm(request.POST or None, instance=user)
        profile_form = ProfileUpdate_CreateForm(
            request.POST or None, request.FILES or None, instance=profile)
        context = {'user_form': user_form, 'profile_form': profile_form,
                'profile': user.profile, 'user': user}
        if profile_form.is_valid():
            profile_form.save()
            user_form.save()
            add_message(request, SUCCESS, 'Profile updated successfully')
            return (redirect(reverse('accounts:profile', args=(id,))))
        return render(request, 'accounts/profile_update.html', context)
    return HttpResponseForbidden()

def PassChange(request, id):
    user = get_object_or_404(User, id=id)
    if request.user == user or request.user.is_staff:
        form = PassChangeForm(user, data=request.POST or None)
        context = {'user': user, 'form': form}

        if form.is_valid():
            form.save()
            add_message(request, SUCCESS, 'Password updated succesfully')
            login(request, user)
            return redirect('home')
        return render(request, 'accounts/password_change.html', context)
    return HttpResponseForbidden()


