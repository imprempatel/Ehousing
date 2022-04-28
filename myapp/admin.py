from django.contrib import admin

from clientapp.models import Ads, Maintenance, Member,Club,Complaint
from .models import *

admin.site.site_header = "E-Housing Admin"
admin.site.site_title = "E-Housing Admin Portal"
admin.site.index_title = "Welcome to E-Housing Portal"
# Register your models here.

admin.site.register(User)
admin.site.register(Member)
admin.site.register(Ads)
admin.site.register(Club)
admin.site.register(Event)
admin.site.register(Complaint)
admin.site.register(Maintenance)
