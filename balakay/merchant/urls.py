from django.urls import path
from .views import (
    register_partner,
    login_partner,
    manage_schedule,
    add_schedule,
    edit_schedule,
    schedule_details,
    center_profile,
    cancel_booking,
    logout_partner
)
from .views import SectionAPIView, ScheduleAPIView

urlpatterns = [
    path('register/', register_partner, name='register_partner'),
    path('', login_partner, name='login_partner'),
    path('schedule/', manage_schedule, name='manage_schedule'),
    path('schedule/add/', add_schedule, name='add_schedule'),
    path('schedule/<int:schedule_id>/edit/', edit_schedule, name='edit_schedule'),
    path('schedule/<int:schedule_id>/', schedule_details, name='schedule_details'),
    path('center_profile/', center_profile, name='center_profile'),
    path('sections/', SectionAPIView.as_view(), name='sections-api'),
    path('schedules/', ScheduleAPIView.as_view(), name='schedules-api'),
    path('logout/', logout_partner, name='logout_partner'),
    path('schedule/<int:booking_id>/cancel/', cancel_booking, name='cancel_booking'),
]