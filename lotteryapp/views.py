from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def main(request):
    return render(request, "main.html")

@login_required
def about(request):
    return render(request, "about.html")



@login_required
def share(request):
    #model에서 share에 해당하는 친구들 찾아서 템플릿 태그로 전달할 수 있게 준비!
    examples = ["share1", "share2"]
    return render(request, "main.html", {'examples' : examples} )

@login_required
def share_detail(request, pk):
    return render(request, "share_detail.html")



@login_required    
def request(request):
    #model에서 request에 해당하는 친구들 찾아서 템플릿 태그로 전달할 수 있게 준비!
    examples = ["request1", "request2"]
    return render(request, "main.html", {'examples' : examples})

@login_required
def request_detail(request, pk):
    return render(request, "request_detail.html")



@login_required
def write(request):
    return render(request, "write.html")

@login_required
def write_share(request):
    #form 태그에 입력값이 들어오면 모델에서 처리해준후, 메인페이지 리다이렉트
    if request.POST:
        return redirect(main)
    return render(request, "write_share.html")

@login_required
def write_request(request):
    #form 태그에 입력값이 들어오면 모델에서 처리해준후, 메인페이지 리다이렉트
    if request.POST:
        #DB생성하는 과정
        return redirect(main)
    return render(request, "write_request.html")

