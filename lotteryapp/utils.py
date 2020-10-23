from .models import *
from datetime import datetime
import numpy as np

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

    limit_hour = int(target.limit_time[0] + target.limit_time[1])
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


# 발주량과 Share/Request 내역을 정리합니다.
# ML module에 들어가기 전에 필요합니다.
# 현재 유저와 정리할 item 이름을 parameter로 받습니다.
def calibrate_RS_data(current_user, item):
    order_list   = OrderItem.objects.filter(author=current_user).filter(item_name=item)

    # 만약 발주 내역이 10일 미만인 경우 데이터가 충분하지 않은 것으로 판단합니다.
    if len(order_list) < 10:
        return None

    result = []

    for order in order_list:
        target_date = order.order_date
        share_num = 0
        request_num = 0

        try:
            share_target = ItemShare.objects.filter(author=current_user).filter(item=item).get(dates=target_date)
            share_num = share_target.item_num
        except ItemShare.DoesNotExist:
            share_num = 0

        try:
            request_target = ItemRequest.objects.filter(author=current_user).filter(item=item).get(dates=target_date)
            request_num = request_target.item_num
        except ItemRequest.DoesNotExist:
            request_num = 0

        diff = share_num - request_num
        result.append([order.item_num, diff])

    print(result)
    return np.array(result)