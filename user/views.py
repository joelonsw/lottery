from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import UserForm
from lotteryapp.utils import get_location_coordinate

# SMTP 관련 인증
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_text
from .tokens import account_activation_token

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
                # 위도, 경도 초기화를 위해 넣었습니다. -현준-
                lat, lng = get_location_coordinate(request.POST['address'])
                user.profile.latitude = lat
                user.profile.longitude = lng

                # 이메일 인증
                # user.is_active = False # 유저 비활성화
                user.save()
                # current_site = get_current_site(request) 
                # message = render_to_string('activation_email.html', {
                #     'user': user,
                #     'domain': current_site.domain,
                #     'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                #     'token': account_activation_token.make_token(user),
                # })
                # mail_title = "계정 활성화 확인 이메일"
                # mail_to = request.POST['email']
                # email = EmailMessage(mail_title, message, to=[mail_to])
                # email.send()
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

# def activate(request, uidb64, token):
#     try:
#         uid = force_text(urlsafe_base64_decode(uidb64))
#         user = User.objects.get(pk=uid)
#     except(TypeError, ValueError, OverflowError, User.DoesNotExsit):
#         user = None
#     if user is not None and account_activation_token.check_token(user, token):
#         user.is_active = True
#         user.save()
#         return render(request, 'home.html', {'alert' : 3})
#     else:
#         return render(request, 'home.html', {'alert' : 4})