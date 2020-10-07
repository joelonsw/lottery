from .models import *
from datetime import datetime


def update_outdate():
    live_requests = ItemRequest.objects.filter(outdate=True)


def update_remain(num, target):
    target.remain -= num
    target.save()