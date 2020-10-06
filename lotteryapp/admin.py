from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(ItemRequest)
admin.site.register(ItemShare)
admin.site.register(RequestAccept)
admin.site.register(ShareAccept)