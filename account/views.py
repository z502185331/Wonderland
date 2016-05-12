from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate

from forms import RestristrationForm
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from models import *

def loginPage(request):
    '''
    A method to load the login/register page
    '''
    if request.user.is_authenticated():
        return redirect(reverse('profile'))
    
    loginForm = AuthenticationForm()  # form for users to login
    registerForm = RestristrationForm()  # form for users to register
    
    context = {'loginForm' : loginForm, 'registerForm' : registerForm}
    return render(request, 'page/login.html', context)


@login_required
def profilePage(request):
    '''
    A method to load the profile page, which is after the login
    '''
    return render(request, 'page/index.html', {})
    

def onLogin(request):
    '''
    A method to login(username and password)
    '''
    form = AuthenticationForm(data = request.POST)
    
    # Check the valid of Form
    if not form.is_valid():
        return render(request, 'page/login.html', 
                      {'loginForm' : form, 'registerForm' : RestristrationForm()})
    
    # login the user
    login(request, form.get_user())
    return redirect(reverse('profile'))


@login_required
def onLogout(request):
    '''
    A method to logout current account and return to the login page
    '''
    logout(request)
    return redirect(reverse('loginIndex'))


def onRegister(request):
    '''
    A method to register a new account
    '''
    form = RestristrationForm(request.POST)
    if not form.is_valid():
        return render(request, 'page/login.html',
                      {'loginForm' : AuthenticationForm(), 'registerForm' : form})
    
    # Create new account
    user = User()
    user.username = form.cleaned_data['username']
    user.set_password(form.cleaned_data['password'])
    user.email = form.cleaned_data['email']
    user.save()
    
    # Init a user info
    ui = UserInfo()
    ui.user = user
    ui.save()
    
    # Login
    user = authenticate(username = form.cleaned_data['username'], password = form.cleaned_data['password'])
    login(request, user)
    return redirect(reverse('profile'))
    

    