from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import UserForm
from lotteryapp.models import *
from lotteryapp.mlmodule import *
from lotteryapp.utils import *
import numpy as np
from lotteryapp.utils import *
from datetime import datetime

# SMTP 관련 인증
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_text
from .tokens import account_activation_token
from django.contrib.auth.decorators import login_required


# Create your views here.
def home(request):
    return render(request, "home.html")

@login_required
def mypage(request):
    update_outdate()
    current_user = Profile.objects.get(user=request.user.pk)
    order_list   = OrderItem.objects.filter(author=current_user)
    order_list   = sorted(order_list, key=lambda target: target.order_date)
    share_list   = ItemShare.objects.filter(author=current_user)
    share_list   = sorted(share_list, key=lambda target: target.dates)
    request_list = ItemRequest.objects.filter(author=current_user)
    request_list = sorted(request_list, key=lambda target: target.dates)
    today        = datetime.now()

    ml_returning = {}

    for item in whole_item:
        status = ""
        ml_model = LinearFitting(item)
        processed = calibrate_RS_data(current_user, item)

        if len(processed) > 0:
            ml_model.get_line_from_data(processed)
            try:
                today_order = OrderItem.objects.filter(author=current_user).filter(item_name=item).get(order_date=today)
                prediction = ml_model.fitting(today_order.item_num)

                if prediction < today_order.item_num / 100 * 5 and prediction > today_order.item_num / 100 * (-5):
                    status = "적정"
                elif prediction >= today_order.item_num / 100 * 5:
                    status = "과잉"
                else:
                    status = "부족"
                
                tomorrow = today_order.item_num
                ml_returning[item] = {"status" : status, "tomorrow" : tomorrow}
            except OrderItem.DoesNotExist:
                pass

    return render(request, "mypage.html", {"order_list" : order_list, "share_list" : share_list, "request_list" : request_list, "ml_returning" : ml_returning})


def signup(request):
    if request.method == "POST":
        if request.POST['password'] == request.POST['password_confirm']:
            filled_form = UserForm(request.POST)
            if request.POST['location'] != "":
                if filled_form.is_valid():
                    user = User.objects.create_user(username=request.POST['username'], password = request.POST['password'], email = request.POST['email'])
                    user.profile.fullname = request.POST['fullname']
                    user.profile.location = request.POST['location']
                    user.profile.phone = request.POST['phone']
                    if request.POST['location'] == "강남역점":
                        user.profile.address = "서울 강남구 강남대로 376"
                    if request.POST['location'] == "대치점":
                        user.profile.address = "서울 강남구 도곡로 460"
                    if request.POST['location'] == "서울대입구역점":
                        user.profile.address = "서울 관악구 관악로 202"
                    if request.POST['location'] == "사당점":
                        user.profile.address = "서울 관악구 과천대로 947 사당타워"
                    if request.POST['location'] == "코엑스몰점":
                        user.profile.address = "서울 강남구 봉은사로 524 코엑스"
                    if request.POST['location'] == "남부터미널점":
                        user.profile.address = "서울 서초구 효령로 292 서울남부터미널 상가 1층"
                    if request.POST['location'] == "유니스트점":
                        user.profile.address = "울산광역시 울주군 언양읍 유니스트길 50"
                    # 위도, 경도 초기화를 위해 넣었습니다. -현준-
                    lat, lng = get_location_coordinate(user.profile.address)
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
                return render(request, "signup.html", {'alert' : 3})
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