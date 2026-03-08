from django.urls import path
from . import views

urlpatterns = [
    path('book/', views.book_appointment, name='book_appointment'),
    path('success/', views.appointment_success, name='appointment_success'),
    path('doctor/', views.doctor_dashboard, name='doctor_dashboard'),
    path('update-status/<int:appointment_id>/', views.update_status, name='update_status'),
    path('login-redirect/', views.login_redirect, name='login_redirect'),
]