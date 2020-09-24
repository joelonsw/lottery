from django.shortcuts import render, redirect

# Create your views here.
def home(request):
    return render(request, "home.html")

def main(request):
    return render(request, "main.html")

def share(request):
    #model에서 share에 해당하는 친구들 찾아서 템플릿 태그로 전달할 수 있게 준비!
    examples = ["share1", "share2"]
    return render(request, "main.html", {'examples' : examples} )
    
def request(request):
    #model에서 share에 해당하는 친구들 찾아서 템플릿 태그로 전달할 수 있게 준비!
    examples = ["request1", "request2"]
    return render(request, "main.html", {'examples' : examples})

def detail(request):
    #객채의 id를 인자로 넘겨받아야 할 것.
    #primaryKey로 해당 객채의 id를 받아, share인지 request인지 조회해서 성격을 넘겨줄 것
    return render(request, "detail.html", {'category' : "shared"})

def share_response(request):
    #객채의 id를 인자로 넘겨받아야 할 것.
    #primaryKey로 해당 객체 id로 조회해서 보여주고 Form태그로 요청이 들어오면 DB수정해서 보여줄 것
    if request.POST:
        #DB update
        return redirect(main)
    return render(request, "share_response.html")

def request_response(request):
    #객채의 id를 인자로 넘겨받아야 할 것.
    #primaryKey로 해당 객체 id로 조회해서 보여주고 Form태그로 요청이 들어오면 DB수정해서 보여줄 것
    if request.POST:
        #DB update
        return redirect(main)    
    return render(request, "request_response.html")


def write(request):
    return render(request, "write.html")

def write_share(request):
    #form 태그에 입력값이 들어오면 모델에서 처리해준후, 메인페이지 리다이렉트
    if request.POST:
        return redirect(main)
    return render(request, "write_share.html")

def write_request(request):
    #form 태그에 입력값이 들어오면 모델에서 처리해준후, 메인페이지 리다이렉트
    if request.POST:
        return redirect(main)
    return render(request, "write_request.html")

