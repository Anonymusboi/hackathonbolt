# backend/urls.py
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'), # Home page
    
    # Authentication
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Profile setup
    path('profile-type/', views.profile_type, name='profile_type'),
    path('jobseeker-profile/', views.job_seeker_profile, name='jobseeker_profile'),
    path('employer-profile/', views.employer_profile, name='employer_profile'),
    
    # Dashboards
    path('dashboard/', views.dashboard, name='dashboard'),
    path('jobseeker-dashboard/', views.job_seeker_dashboard, name='jobseeker_dashboard'),
    path('employer-dashboard/', views.employer_dashboard, name='employer_dashboard'),
    
    # Job postings
    path('post-job/', views.post_job, name='post_job'),
    
    # Applications
    path('apply-job/<int:job_id>/', views.apply_job, name='apply_job'),
    path('my-applications/', views.view_applications, name='view_applications'),
]