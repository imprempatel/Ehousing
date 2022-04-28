from django.urls import path
from . import views

urlpatterns = [
    path('',views.sign_in,name='sign-in'),
    path('index/',views.index,name='index'),
    path('sign-up/',views.sign_up,name='sign-up'),
    path('otp/',views.otp,name='otp'),
    path('logout/',views.logout,name='logout'),
    path('forgot-password/',views.forgot_password,name='forgot-password'),
    path('profile/',views.profile,name='profile'),
    path('change-password/',views.change_password,name='change-password'),
    path('add-member/',views.add_member,name='add-member'),
    path('events/',views.events,name='events'),
    path('view-maintenance/',views.view_maintenance,name='view-maintenance'),
    path('edit-event/<int:pk>',views.edit_event,name='edit-event'),
    path('delete-event/<int:pk>',views.delete_event,name='delete-event'),
    path('view-complaint/<int:pk>',views.view_complaint,name='view-complaint'),
    path('resolve-complaint/<int:pk>',views.resolve_complaint,name='resolve-complaint'),
    path('search-maintenance/',views.search_maintenance,name='search-maintenance'),

]
