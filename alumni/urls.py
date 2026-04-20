from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    # Alumni
    path('alumni/', views.alumni_list, name='alumni_list'),
    path('alumni/create/', views.alumni_create, name='alumni_create'),
    path('alumni/<int:pk>/', views.alumni_detail, name='alumni_detail'),
    path('alumni/<int:pk>/update/', views.alumni_update, name='alumni_update'),
    # Jobs
    path('jobs/', views.job_list, name='job_list'),
    path('jobs/create/', views.job_create, name='job_create'),
    path('jobs/<int:pk>/', views.job_detail, name='job_detail'),
    path('jobs/<int:pk>/apply/', views.job_apply, name='job_apply'),
    # Applications
    path('my-applications/', views.my_applications, name='my_applications'),
    path('my-applications/<int:pk>/withdraw/', views.withdraw_application, name='withdraw_application'),
    # Events
    path('events/', views.event_list, name='event_list'),
    path('events/create/', views.event_create, name='event_create'),
    # AI Advisor
    path('ai-advisor/', views.ai_advisor, name='ai_advisor'),
    path('ai-advisor/api/', views.ai_advisor_api, name='ai_advisor_api'),
]