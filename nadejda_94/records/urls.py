from django.urls import path, include
from . import views

urlpatterns = [
    path('login_register/', views.login_page, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('', views.home, name='home'),
    path('<int:pk>/', include([
        path('create-record/', views.create_record, name='create_record' ),
        path('firm-reports/', views.firm_reports, name='firms_reports'),                                                                    ])),

    path('day-reports/', views.day_reports, name='day_reports'),
    path('month-reports/', views.month_reports, name='month_reports'),
    path('new-partner/', views.new_partner, name='new_partner'),
    path('show-totals/', views.show_totals, name='show_totals'),
    path('partner-choice/', views.partner_choice, name='partner_choice'),

]