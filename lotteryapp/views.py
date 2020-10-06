from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from lotteryapp.models import *
import lotteryapp.utils

# Create your views here.

@login_required
def main(request):
    return render(request, "main.html")

##여기서 DB설계와 여기서 보여주는거 뿌리는 거는 @현준님

# outdate 플래그가 활성화 되지 않은 share/request를 필터링 합니다.
# 그 후, 게시 날짜와 시간이 빠른 순서대로 정렬하여 template으로 전송합니다.
@login_required
def share(request):
    target_share_list = ItemShare.objects.filter(outdate=False)
    target_share_list = sorted(target_share_list, key=lambda target: target.dates)
    return render(request, "share.html", {'shares' : target_share_list})

@login_required
def request(request):
    target_request_list = ItemRequest.objects.filter(outdate=False)
    target_request_list = sorted(target_request_list, key=lambda target: target.dates)
    return render(request, "request.html", {'requests' : target_request_list})

##아래 주석처리한 로직을 합쳐 share_detail, request_detail에서 구현해주세요! @ 영규님
##detail 끌어오가나 할떄 인자로 객체 id 파라미터로 끌고 다니셔야합니다!
    # def detail(request):
    #     #객채의 id를 인자로 넘겨받아야 할 것.
    #     #primaryKey로 해당 객채의 id를 받아, share인지 request인지 조회해서 성격을 넘겨줄 것
    #     return render(request, "detail.html", {'category' : "shared"})

    # def share_response(request):
    #     #객채의 id를 인자로 넘겨받아야 할 것.
    #     #primaryKey로 해당 객체 id로 조회해서 보여주고 Form태그로 요청이 들어오면 DB수정해서 보여줄 것
    #     if request.POST:
    #         #DB update
    #         return redirect(main)
    #     return render(request, "share_response.html")

    # def request_response(request):
    #     #객채의 id를 인자로 넘겨받아야 할 것.
    #     #primaryKey로 해당 객체 id로 조회해서 보여주고 Form태그로 요청이 들어오면 DB수정해서 보여줄 것
    #     if request.POST:
    #         #DB update
    #         return redirect(main)    
    #     return render(request, "request_response.html")
@login_required
def share_detail(request):
    return render(request, "share_detail.html")

@login_required
def request_detail(request):
    return render(request, "request_detail.html")


# 끝
@login_required
def write(request):
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