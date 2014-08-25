from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.http import require_GET
from django.views.decorators.http import require_POST

from models import UserProfile

from forms import LoginForm
from forms import RegisterForm

# Create your views here.

def new_user(userdata):
    username = userdata['username']
    password = userdata['password']
    email = userdata['email']
    name = userdata['name']
    birthday = userdata['birthday']
    intro = userdata['intro']
    phone = userdata['phone']
    # photo = Photo.objects.get(id=1)

    user = User(username=username, email=email)
    user.set_password(password)
    user.save()

    profile = UserProfile(user=user, name=name, birthday=birthday, 
                    intro=intro, phone=phone)
    profile.save()

def login_user(request, username, password):
    user = authenticate(username=username, password=password)
    if user:
        login(request, user)
    return user


def get_signup(request):
    form = RegisterForm()
    return render(request, 'sign_up.html', {
            'form': form,
    })

def get_signin(request):
    form = LoginForm()
    return render(request, 'sign_in.html', {
            'form': form,
    })


def post_signup(request):
    form = RegisterForm(request.POST)
    if form.is_valid():
        print 'valid'
        if form.is_registered():
            return HttpResponseRedirect('/')

        userdata = {
            'username': form.cleaned_data['username'],
            'password': form.cleaned_data['passwd'],
            'email': form.cleaned_data['email'],
            'name': form.cleaned_data['name'],
            'birthday': form.cleaned_data['birthday'],
            'intro': form.cleaned_data['intro'],
            'phone': form.cleaned_data['phone']
        }

        new_user(userdata)
        return HttpResponseRedirect('signin')
    print 'invalid'
    
    return HttpResponseRedirect('/')

def post_signin(request):
    form = LoginForm(request.POST)
    if form.is_valid():
        username = form.cleaned_data['user']
        password = form.cleaned_data['password']

        redirect_url = 'http://google.com'
        print username, password

        user = login_user(request, username, password)
        if user:
            profiles = request.user.get_profile()
            redirect_url = '/'
        else: # id not found
            pass
    return HttpResponseRedirect('/')

"""
def sign_up(request):  
    if request.method == 'GET':
        return get_signup(request)
    elif request.method == 'POST':
        return post_signup(request)
"""

def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            print 'valid'
            if form.is_registered():
                return HttpResponseRedirect('/')

            userdata = {
                'username': form.cleaned_data['username'],
                'password': form.cleaned_data['passwd'],
                'email': form.cleaned_data['email'],
                'name': form.cleaned_data['name'],
                'birthday': form.cleaned_data['birthday'],
                'intro': form.cleaned_data['intro'],
                'phone': form.cleaned_data['phone']
            }

            new_user(userdata)
            return HttpResponseRedirect('/')

    else:
        form = RegisterForm()

    return render(request, 'sign_up.html', {
            'form': form,
    })
    

def sign_in(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    
    if request.method == "POST":
        username = request.POST.get('user', None)
        password = request.POST.get('password', None)
        next = request.POST.get('next', '/')
        
        if username and password: # valid
            user = login_user(request, username, password)
            if user:
                profiles = request.user.get_profile()
                return HttpResponseRedirect(next)
                
            else: # id not found or password wrong
                message = 'Account not found'
        else:
            message = 'Please fill in the blanks'
    else:
        next = request.GET.get('next')
        username = ''
        message = ''
    print locals()
    return render(request, 'signin.html', {
        'username': username,
        'message': message,
        'next': next,
    })
        
        
def sign_out(request):
    logout(request)
    return HttpResponseRedirect('/')
