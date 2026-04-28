from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import test_api, student_list_create, student_details

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), 
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('test/', test_api),
    path("students/", student_list_create),
    path("students/<int:pk>/", student_details),
    path('api/', include('jobboard.urls')),
]