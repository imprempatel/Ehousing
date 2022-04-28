from django.urls import path
from . import views

urlpatterns = [
    path('',views.login,name='login'),
    path('index/',views.clientindex,name='client-index'),
    path('house-details/',views.house_details,name='house-details'),
    path('change-member-password/',views.change_member_password,name='change-member-password'),
    path('advertise/',views.advertise,name='advertise'),
    path('view-ad-details/<int:pk>',views.ad_details,name='view-ad-details'),
    path('complaint/',views.complaint,name='complaint'),
    path('maintenance/',views.maintenance,name='maintenance'),
    path('member-logout/',views.member_logout,name='member-logout'),
    path('maintenance/paymenthandler/<int:pk>', views.paymenthandler, name='paymenthandler'),
    # path('book-club-hall/',views.book_club_hall,name='book-club-hall'),
]
