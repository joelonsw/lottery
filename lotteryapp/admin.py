from django.contrib import admin
from lotteryapp.models import DummyRequest, DummyShare

# Register your models here.
admin.site.register(DummyRequest)
admin.site.register(DummyShare)