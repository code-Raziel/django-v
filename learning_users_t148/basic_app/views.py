from django.shortcuts import render
from basic_app.forms import UserForm,UserProfileInfoForm
#
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect, HttpResponse
# DEPRECATED : from django.core.urlresolvers import reverse
# Importing from the django.core.urlresolvers module is deprecated in favor of its new location, django.urls.
# https://github.com/django-import-export/django-import-export/issues/598
# https://docs.djangoproject.com/en/dev/releases/1.10/#deprecated-features-1-10
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request,'basic_app/index.html')

def special(request):
    return HttpResponse("You Are logged in, Nice!")

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register(request):
    registered = False

    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form=UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()
            registered = True

        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request,'basic_app/registration.html',
                                {   'user_form':user_form,
                                    'profile_form':profile_form,
                                    'registered':registered})

def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)

        #https://stackoverflow.com/questions/20809417/what-does-if-var-mean-in-python
        if user:
            # https://stackoverflow.com/questions/63132624/how-do-i-fix-the-bool-object-is-not-callabe-error-in-my-django-website
            # DEPRECATED : user.is_active() becomes user.is_active:

            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))

            else:
                return HttpResponse("ACCOUNT NOT ACTIVE")
        else:
            print("Someone tried to login and failed!")
            print("Username: {} and password {}".format(username,password))
            return HttpResponse("invalid login details supplied!")
    else:
        return render(request,'basic_app/login.html',{})
