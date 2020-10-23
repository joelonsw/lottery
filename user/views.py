from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import UserForm
from lotteryapp.models import *
from lotteryapp.mlmodule import *
from lotteryapp.utils import *

# Create your views here.
def home(request):
    return render(request, "home.html")


def mypage(request):
    current_user = Profile.objects.get(user=request.user.pk)
    order_list   = OrderItem.objects.filter(author=current_user)
    order_list   = sorted(order_list, key=lambda target: target.dates)
    share_list   = ItemShare.objects.filter(author=current_user)
    share_list   = sorted(share_list, key=lambda target: target.dates)
    request_list = ItemRequest.objects.filter(author=current_user)
    request_list = sorted(request_list, key=lambda target: target.dates)

    return render(request, "mypage.html", {"order_list" : order_list, "share_list" : share_list, "request_list" : request_list})


def signup(request):
    if request.method == "POST":
        if request.POST['password'] == request.POST['password_confirm']:
            filled_form = UserForm(request.POST)
            if filled_form.is_valid() and request.POST['location'] is not "":
                user = User.objects.create_user(username=request.POST['username'], password = request.POST['password'], email = request.POST['email'])
                user.profile.fullname = request.POST['fullname']
                user.profile.location = request.POST['location']
                user.profile.phone = request.POST['phone']
                user.save()
                return render(request, "home.html", {'alert' : 2})
            else:
                return render(request, "signup.html", {'alert' : 2})
        else:
            return render(request, "signup.html", {'alert' : 1})
    return render(request, "signup.html")


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect('main')
        else:
            return render(request, 'home.html', {'alert' : 1})
    else:
        return render(request, 'home.html')


def log_out(request):
    logout(request)
    return redirect('home')