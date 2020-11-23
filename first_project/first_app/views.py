from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from first_app.models import AccessRecord, Topic, Webpage, UserProfileInfo
from first_app.forms import FormName, UserForm, UserProfileInfoForm
from . import forms

from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
# Create your views here.

def home_page(request):
    return render(request, 'first_app/home_page.html')


def user_info(request):
    webpg_list = AccessRecord.objects.order_by('date')
    date_dict = {'access_records': webpg_list}
    return render(request, "first_app/User_information.html", context=date_dict)


def form_page_view(request):
    form = forms.FormName()

    if request.method == 'POST':
        form = forms.FormName(request.POST)
        if form.is_valid():
            print("Validation success")
            print("Name: ", form.cleaned_data['name'])
            print("Email: ", form.cleaned_data['email'])
            print("Text: ", form.cleaned_data['text'])
            print("Date: ", form.cleaned_data['date'])
            print("Respond: ", form.cleaned_data['like'])

    return render(request, 'first_app/form_page.html', {'form': form})


def bob(request):
    return render(request, 'first_app/bob.html')


def search_engines(request):
    context_dict = {'text': "User information exposed", 'number': 200}
    return render(request, 'first_app/search_engines.html', context_dict)


def other(request):
    return render(request, 'first_app/other.html')


@login_required()
def special(request):
    return HttpResponse('You are logged in!')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse("home_page"))


def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)
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
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request, 'first_app/registration.html', {'user_form': user_form,
                                                           'profile_form': profile_form,
                                                           'registered': registered})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('home_page'))
            else:
                return HttpResponse('Account is not active')
        else:
            print('Someone tried to login and failed')
            print('Username: {} and Password: {}'.format(username, password))
            return HttpResponse("Invalid details login supplied")
        print('User is active')
    return render(request, 'first_app/login.html', {})
