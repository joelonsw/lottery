from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from lotteryapp.models import *
from lotteryapp.utils import *
from datetime import datetime
# Create your views here.
# 이메일
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_text

@login_required
def main(request):
    update_outdate()
    target_share_list = ItemShare.objects.filter(outdate=False)
    target_request_list = ItemRequest.objects.filter(outdate=False)
    # urg_Request = []
    # urg_Share = []
    urgent_share_items = []
    urgent_request_items = []

    if len(target_share_list) > 0:

        #급한 Share 선별 1. 가장 시간이 적게 남은 Share.
        target_share_list = sorted(target_share_list, key=lambda target: target.remain_time)
        urgent_share_items.append(target_share_list[0])
        #급한 Share 선별 2. 가장 재고가 많이 남은 Share.
        target_share_list = sorted(target_share_list, key=lambda target: target.remain, reverse=True)
        urgent_share_items.append(target_share_list[0])
    
    if len(target_request_list) > 0:
        #급한 Request 선별 1. 가장 시간이 적게 남은 Request.
        target_request_list = sorted(target_request_list, key=lambda target: target.remain_time)
        urgent_request_items.append(target_request_list[0])
        #급한 Request 선별 2. 가장 재고가 많이 남은 Request.
        target_request_list = sorted(target_request_list, key=lambda target: target.remain, reverse=True)
        urgent_request_items.append(target_request_list[0])


        #urgent_items 리스트 업데이트
        # * urgent_items[0] : 가장 시간이 적게 남은 Request.
        # * urgent_items[1] : 가장 재고가 적게 남은 Share.
        # * urgent_items[2] : 가장 시간이 적게 남은 Request.
        # * urgent_items[3] : 가장 재고가 적게 남은 Share.
        # for i in range (0, len(urg_Request)):
        #     urgent_items.append(urg_Request[i])
        # for i in range (0, len(urg_Share)):
        #     urgent_items.append(urg_Share[i])

    return render(request, "main.html", {'urgent_share_items' : urgent_share_items, 'urgent_request_items' : urgent_request_items})

##여기서 DB설계와 여기서 보여주는거 뿌리는 거는 @현준님

# outdate 플래그가 활성화 되지 않은 share/request를 필터링 합니다.
# 그 후, 게시 날짜와 시간이 빠른 순서대로 정렬하여 template으로 전송합니다.
@login_required
def share(request):
    update_outdate()
    target_share_list = ItemShare.objects.filter(outdate=False)
    target_share_list = sorted(target_share_list, key=lambda target: target.dates)

    current_user         = Profile.objects.get(user=request.user.pk)
    share_ver_location   = sort_by_location(current_user, "share")
    return render(request, "share.html", {'shares' : target_share_list})

@login_required
def request(request):
    update_outdate()
    target_request_list = ItemRequest.objects.filter(outdate=False)
    target_request_list = sorted(target_request_list, key=lambda target: target.dates)

    current_user         = Profile.objects.get(user=request.user.pk)
    request_ver_location = sort_by_location(current_user, "request")
    return render(request, "request.html", {'requests' : target_request_list})

##아래 주석처리한 로직을 합쳐 share_detail, request_detail에서 구현해주세요! @ 영규님
##detail 끌어오가나 할떄 인자로 객체 id 파라미터로 끌고 다니셔야합니다!

# url에 object의 pk_num을 담아 detail 보여주기
@login_required
def share_detail(request, detail_id):
    detail = ItemShare.objects.get(pk=detail_id)
    return render(request, "share_detail.html", {"detail" : detail})

@login_required
def request_detail(request, detail_id):
    detail = ItemRequest.objects.get(pk=detail_id)
    return render(request, "request_detail.html", {"detail" : detail})

@login_required
def share_accept(request, detail_id):
    #객채의 id를 인자로 넘겨받아야 할 것.
    #primaryKey로 해당 객체 id로 조회해서 보여주고 Form태그로 요청이 들어오면 DB수정해서 보여줄 것
    detail = ItemShare.objects.get(pk=detail_id)
    if request.POST:
        #DB update
        share_accept_object = ShareAccept(share_location=request.POST['location'],
                                            share_num=request.POST['num'],
                                            share_email=request.POST['email'],
                                            share_phone=request.POST['phone'],
                                            share_contents=request.POST['content'],

                                            target=detail,
                                            volunteer=request.user)
        share_accept_object.save()
        detail.remain = detail.remain-int(request.POST['num'])
        detail.save()

        # share 이메일 보내기
        current_site = get_current_site(request)
        message = render_to_string('share_email.html', {
            'user': detail.author,
            'request_user': request.user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(request.user.pk)),
            'share': share_accept_object,
            'detail': detail,
        })
        mail_title = request.POST['location'] + "으로부터 " + detail.item + " Share 요청이 들어왔습니다."
        mail_to = detail.email,
        email = EmailMessage(mail_title, message, to=[mail_to])
        email.send()
        return redirect(main)
    return redirect(share_detail, detail_id)

@login_required
def request_accept(request, detail_id):
    #객채의 id를 인자로 넘겨받아야 할 것.
    #primaryKey로 해당 객체 id로 조회해서 보여주고 Form태그로 요청이 들어오면 DB수정해서 보여줄 것
    detail = ItemRequest.objects.get(pk=detail_id)
    if request.POST:
        #DB update
        request_accept_object = RequestAccept(request_location=request.POST['location'],
                                                request_num=request.POST['num'],
                                                request_email=request.POST['email'],
                                                request_phone=request.POST['phone'],
                                                request_contents=request.POST['content'],

                                                target=detail,
                                                volunteer=request.user)
        request_accept_object.save()
        detail.remain = detail.remain-int(request.POST['num'])
        detail.save()

        # request 이메일 보내기
        current_site = get_current_site(request)
        message = render_to_string('request_email.html', {
            'user': detail.author,
            'request_user': request.user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(request.user.pk)),
            'request': request_accept_object,
            'detail': detail,
        })
        mail_title = request.POST['location'] + "으로부터 " + detail.item + " Request 요청이 들어왔습니다."
        mail_to = detail.email,
        email = EmailMessage(mail_title, message, to=[mail_to])
        email.send()
        return redirect(main)    
    return redirect(share_detail, detail_id)
# 끝
@login_required
def write(request):
    update_outdate()
    return render(request, "write.html")

# POST인 경우 model instance 만들고 save.
# current의 경우 request.user가 현재 로그인 중인 유저를 가리키는 것 같음
# ItemShare와 ItemRequest가 foreign key를 Profile로 받기 때문에 pk로 서치해서 사용함.
@login_required
def write_share(request):
    if request.POST:
        current_user = Profile.objects.get(user=request.user.pk)
        share_post = ItemShare(location=request.POST['location'],
                                item=request.POST['item'],
                                item_num=request.POST['item_num'],
                                limit_time=request.POST['limit_time'],
                                email=request.POST['email'],
                                phone=request.POST['phone'],
                                contents=request.POST['contents'],
                                author=current_user,
                                remain=request.POST['item_num'])
        share_post.save()
        return redirect(main)
    return render(request, "write_share.html")

@login_required
def write_request(request):
    if request.POST:
        current_user = Profile.objects.get(user=request.user.pk)
        request_post = ItemRequest(location=request.POST['location'],
                                   item=request.POST['item'],
                                   item_num=request.POST['item_num'],
                                   limit_time=request.POST['limit_time'],
                                   email=request.POST['email'],
                                   phone=request.POST['phone'],
                                   contents=request.POST['contents'],
                                   author=current_user,
                                   remain=request.POST['item_num'])
        request_post.save()
        return redirect(main)
    return render(request, "write_request.html")

# 끝
@login_required
def about(request):
    return render(request, "about.html")