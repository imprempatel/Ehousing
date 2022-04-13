from django.urls import path
from . import views

urlpatterns = [
    path('',views.login,name='login'),
    path('index/',views.clientindex,name='client-index'),
    path('house-details/',views.house_details,name='house-details'),
    path('change-member-password/',views.change_member_password,name='change-member-password'),
    path('advertise/',views.advertise,name='advertise'),
    path('view-ad-details/<int:pk>',views.ad_details,name='view-ad-details'),
]
