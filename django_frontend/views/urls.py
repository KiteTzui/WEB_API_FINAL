from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('rooms/', views.rooms, name='rooms'),
    path('rooms/<int:room_id>/', views.room_details, name='room_details'),
    path('booking/', views.booking, name='booking'),
    path('staff-admin/', views.admin_dashboard, name='admin_dashboard'),
    path('staff-admin/rooms/', views.admin_rooms, name='admin_rooms'),
    path('staff-admin/bookings/', views.admin_bookings, name='admin_bookings'),
    path('staff-admin/users/', views.admin_users, name='admin_users'),
    path('staff-admin/settings/', views.admin_settings, name='admin_settings'),
]
