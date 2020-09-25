from django.shortcuts import render

# Create your views here.
def mypage(request):
    #model에서 적절한 값들을 해당 user에 알맞게 끌어와서 템플릿태그로 넘겨주기
    return render(request, "mypage.html")