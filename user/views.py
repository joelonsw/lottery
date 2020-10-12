from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import UserForm

# Create your views here.
def home(request):
    return render(request, "home.html")

def mypage(request):
    #model에서 적절한 값들을 해당 user에 알맞게 끌어와서 템플릿태그로 넘겨주기
    return render(request, "mypage.html")

def signup(request):
    if request.method == "POST":
        if request.POST['password'] == request.POST['password_confirm']:
            filled_form = UserForm(request.POST)
            if filled_form.is_valid() and request.POST['location'] is not "":
                user = User.objects.create_user(username=request.POST['username'], password = request.POST['password'], email = request.POST['email'])
                user.profile.fullname = request.POST['fullname']
                user.profile.location = request.POST['location']
                user.profile.phone = request.POST['phone']
                user.profile.address = request.POST['address']
                user.profile.address_detail = request.POST['address_detail']
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