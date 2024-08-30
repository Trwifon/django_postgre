from django.urls import path
from . import views

urlpatterns = [
    path('login_register/', views.login_page, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('', views.home, name='home'),
    path('create-record/', views.create_record, name='create_record'),
    path('day-reports/', views.day_reports, name='day_reports'),
    path('firm-reports/', views.firm_reports, name='firms_reports'),
    path('show-totals/', views.show_totals, name='show_totals'),
]