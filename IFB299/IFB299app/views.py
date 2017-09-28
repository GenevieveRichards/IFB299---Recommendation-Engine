from django.shortcuts import render
from django.http import HttpResponse
from .forms import RegisterForm, ProfileForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
import requests

# Create your views here.
def index(request):
	return render(request, 'IFB299app/index.html')


def createaccount(request):
	return render(request, 'IFB299app/createaccount.html')


def login_view(request):
	return render(request, 'IFB299app/login.html')


def dashboard(request):
	return render(request, 'IFB299app/dashboard.html')


def location(request, location_name_slug):
    context_dict = {}

    url = "https://maps.googleapis.com/maps/api/place/details/json?placeid=ChIJ70tS1ZJZkWsR9Dnb1Gm82s0&key=AIzaSyBvXpcHlbpL_ESnnNOm07nBCd1LhpZOSzw" 
    response = requests.get(url) 
    file = response.json() 
    
    #print(file)

    context_dict['name'] = file['result']['name'] 
    context_dict['place_id'] = file['result']['place_id'] 
    context_dict['formatted_address']  = file['result']['formatted_address'] 
    context_dict['formatted_phone_number']  = file['result']['formatted_phone_number'] 
    context_dict['rating']  = file['result']['rating'] 
    context_dict['website']  = file['result']['website'] 
    context_dict['price_level']  = file['result']['price_level'] 
    context_dict['Monday'] = file['result']['opening_hours']['weekday_text'][0]
    context_dict['Tuesday'] = file['result']['opening_hours']['weekday_text'][1]
    context_dict['Wednesday'] = file['result']['opening_hours']['weekday_text'][2]
    context_dict['Thursday'] = file['result']['opening_hours']['weekday_text'][3]
    context_dict['Friday'] = file['result']['opening_hours']['weekday_text'][4]
    context_dict['Saturday'] = file['result']['opening_hours']['weekday_text'][5]
    context_dict['Sunday'] = file['result']['opening_hours']['weekday_text'][6]
    context_dict['Photo']= 'https://maps.googleapis.com/maps/api/place/photo?maxwidth=500&maxheight=500&key=AIzaSyBvXpcHlbpL_ESnnNOm07nBCd1LhpZOSzw&photoreference=' + file['result']['photos'][0]['photo_reference']
    context_dict['Photo2']= 'https://maps.googleapis.com/maps/api/place/photo?maxwidth=500&key=AIzaSyBvXpcHlbpL_ESnnNOm07nBCd1LhpZOSzw&photoreference=' + file['result']['photos'][1]['photo_reference']
    context_dict['Photo3']= 'https://maps.googleapis.com/maps/api/place/photo?maxwidth=500&key=AIzaSyBvXpcHlbpL_ESnnNOm07nBCd1LhpZOSzw&photoreference=' + file['result']['photos'][2]['photo_reference']
    context_dict['Photo4']= 'https://maps.googleapis.com/maps/api/place/photo?maxwidth=500&key=AIzaSyBvXpcHlbpL_ESnnNOm07nBCd1LhpZOSzw&photoreference=' + file['result']['photos'][3]['photo_reference']
    context_dict['Photo5']= 'https://maps.googleapis.com/maps/api/place/photo?maxwidth=500&key=AIzaSyBvXpcHlbpL_ESnnNOm07nBCd1LhpZOSzw&photoreference=' + file['result']['photos'][4]['photo_reference']
    return render(request, 'IFB299app/location.html', context_dict)

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if form.is_valid() and profile_form.is_valid():
            new_user = form.save()
            profile = profile_form.save(commit=False)

            if profile.user_id is None:
                profile.user_id = new_user.id

            profile_form.save()

            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/IFB299app/dashboard/')
    else:
        form = RegisterForm()
        profile_form = ProfileForm()
    return render(request, 'IFB299app/register.html', {
        'form': form,
        'profile_form': profile_form
        })
