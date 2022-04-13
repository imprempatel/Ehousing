from django.contrib import admin

from clientapp.models import Ads, Member,Club
from .models import *

# Register your models here.

admin.site.register(User)
admin.site.register(Member)
admin.site.register(Ads)
admin.site.register(Club)
admin.site.register(Event)
