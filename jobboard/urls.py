from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('jobs/', views.JobListCreateView.as_view(), name='job-list-create'),
    path('jobs/<int:pk>/', views.JobDetailView.as_view(), name='job-detail'),
    path('jobs/my/', views.EmployerJobsView.as_view(), name='employer-jobs'),
    path('jobs/<int:job_id>/applications/', views.JobApplicationsView.as_view(), name='job-applications'),
    path('applications/', views.ApplicationCreateView.as_view(), name='apply'),
    path('applications/my/', views.MyApplicationsView.as_view(), name='my-applications'),
    path('applications/<int:pk>/status/', views.ApplicationStatusView.as_view(), name='application-status'),
]
