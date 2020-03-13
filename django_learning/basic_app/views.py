from django.shortcuts import render
from .forms import UserForm, UserProfileInfoForm


from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

# Create your views here.


def index(request):
    return render(request, 'basic_app/index.html')


@login_required
def special_method(request):
    return HttpResponse('You Are Logedin. Great. Yeah?')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))




def registration(request):
    
    registerd = False
    
    if request.method == 'POST':
        print('first_if_pass')
        
        
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            
            profile = profile_form.save(commit=False)
            profile.user = user
            print('second_if_pass')

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()

            registerd = True
        else:
            print(user_form.errors, profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
        print('we are in last else')
    print('very succesful')
    return render(request, 'basic_app/registration.html', {'user_form' : user_form, 'profile_form' : profile_form, 'registerd' : registerd})

            
            

def user_login(request):
    
    print('Started')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print('post_method')
        user = authenticate(username=username, password=password)
        if user:
            print('authrnticated')
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse('<h2>ACCOUNT IS NOT ACTIVE</h2>')
        else:
            print('wrong username or password. username is {}  and the password is {}  .'.format(username, password))
            return HttpResponse('Wrong UserName Or Password')
    else:
        return render(request, 'basic_app/login.html', {})