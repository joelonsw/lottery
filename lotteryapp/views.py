from django.shortcuts import render, redirect

# Create your views here.
def main(request):
    return render(request, "main.html")

##여기서 DB설계와 여기서 보여주는거 뿌리는 거는 @현준님
def share(request):
    #model에서 share에 해당하는 친구들 찾아서 템플릿 태그로 전달할 수 있게 준비!
    examples = ["share1", "share2"]
    return render(request, "share.html", {'examples' : examples} )
    
def request(request):
    #model에서 request에 해당하는 친구들 찾아서 템플릿 태그로 전달할 수 있게 준비!
    examples = ["request1", "request2"]
    return render(request, "request.html", {'examples' : examples})

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
def share_detail(request):
    return render(request, "share_detail.html")

def request_detail(request):
    return render(request, "request_detail.html")

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
        #DB생성하는 과정
        return redirect(main)
    return render(request, "write_request.html")

def about(request):
    return render(request, "about.html")