from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from .forms import UserForm

# Create your views here.
def home(request):
    return render(request, "home.html")

def mypage(request):
    #model에서 적절한 값들을 해당 user에 알맞게 끌어와서 템플릿태그로 넘겨주기
    return render(request, "mypage.html")

def signup(request):
    regi_form = UserCreationForm()
    if request.method == "POST":
        filled_form = UserCreationForm(request.POST)
        if filled_form.is_valid():
            filled_form.save()
            return redirect('main')
    return render(request, "signup.html", {'regi_form' : regi_form})

def signin(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect('main')
        else:
            return render(request, 'home.html', {'alert' : 1})
    else:
        form = UserForm()
        return render(request, 'home.html')

def log_out(request):
    logout(request)
    return redirect('home')