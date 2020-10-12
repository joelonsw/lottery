from .models import *
from datetime import datetime

# 현재 시간과 비교해서 유효한 시간을 갖는지 검사합니다.
# 유효한 시간이 아니면 False를, 아직 유효하다면 True를 반환합니다.
# ex1) 생성된 model이 2020-10-09에 생성되었고, 현재 날짜가 2020-10-10이면 유효하지 않습니다. -> False
# ex2) 생성된 model이 2020-10-09 8시에 생성되었고, 10시까지 게시한다고 했을때,
# 현재 시간이 2020-10-09 9시이면 유효합니다. -> True
def time_vaild_check(target):
    now_time = datetime.now()

    if target.dates.year  != now_time.year or \
       target.dates.month != now_time.month or \
       target.dates.day   != now_time.day:
        return False

    limit_hour   = int(target.limit_time[0] + target.limit_time[1])
    limit_minute = int(target.limit_time[3] + target.limit_time[4])

    limit_ = datetime(now_time.year, now_time.month, now_time.day, limit_hour, limit_minute, 0, 0)

    if now_time > limit_:
        return False
    else:
        delta = limit_ - now_time
        target.remain_time = delta.seconds
        target.save()

    return True


# 남은 request/share 개수가 0이 되거나 시간이 지나 만료된 게시물 모델을 업데이트 합니다.
# 위 조건에 해당하는 경우, outdate를 True로 만듭니다.
def update_outdate():
    live_requests = ItemRequest.objects.filter(outdate=False)
    live_shares   = ItemShare.objects.filter(outdate=False)

    for obj in live_requests:
        if obj.remain <= 0 or time_vaild_check(obj) == False:
            obj.outdate = True
            obj.save()

    for obj in live_shares:
        if obj.remain <= 0 or time_vaild_check(obj) == False:
            obj.outdate = True
            obj.save()


# target으로 들어온 model에 num 수만큼 remain을 감소 시킵니다.
# remain이 0보다 같거나 작아지면 outdate를 True로 바꿔줍니다. (최대한 search를 줄이기 위해)
def update_remain(num, target):
    if target.remain - num >= 0:
        target.remain -= num
        if target.remain <= 0:
            target.outdate = True
        target.save()


# Google API를 이용해 주소를 파라미터로 받으면 위도/경도로 변환해주는 함수입니다.
# requests 모듈이 추가적으로 필요합니다. (urllib는 python3 기준으로 자동 탑재)
# (Google API가 네이버나 카카오에 비해 파싱을 더 잘 한다고 합니다.)
# API 계정이 무료 버전이기 때문에 200일 정도만 쓸 수 있습니다.
import requests
from urllib.parse import quote

def get_location_coordinate(target):

    location = quote(target)
    URL      = 'https://maps.googleapis.com/maps/api/geocode/json?key=AIzaSyCHDqJNPiWkR0Tl5Hp1HZ11qY6aoyv3V28&sensor=false&language=ko&address={}'.format(location)
    response = requests.get(URL)
    result   = response.json()

    latitude  = result['results'][0]['geometry']['location']['lat']
    longitude = result['results'][0]['geometry']['location']['lng']

    return latitude, longitude


# 현재 유저 위치를 기준으로 request와 share의 item들을 정렬 합니다.
# harversine 모듈이 필요합니다. (pip 버전 20.X 이상에서 다운로드 가능합니다.)
# 현재 위치와 outdate가 False인 item들의 author의 위치를 참조해서 harversine을 적용합니다.
from haversine import haversine

def sort_by_location(current_user, selection):

    current_location = (current_user.latitude, current_user.longitude)

    if selection == "request":
        request_list     = ItemRequest.objects.filter(outdate=False)
        request_return   = []

        for item in request_list:
            if item.author != current_user:
                item_location = (item.author.latitude, item.author.longitude)
                distance      = harersine(current_location, item_location, unit='km')
                tmp_pair      = (item, distance)
                request_return.append(tmp_pair)

        request_sort    = sorted(request_return, key=lambda target: target[1])
        request_result  = [item[0] for item in request_sort]
        return request_result

    elif selection == "share":
        share_list       = ItemShare.objects.filter(outdate=False)
        share_return     = []

        for item in share_list:
            if item.author != current_user:
                item_location = (item.author.latitude, item.author.longitude)
                distance      = haversine(current_location, item_location, unit='km')
                tmp_pair      = (item, distance)
                share_return.append(tmp_pair)

        share_sort      = sorted(share_return, key=lambda target: target[1])
        share_result    = [item[0] for item in share_sort]
        return share_result