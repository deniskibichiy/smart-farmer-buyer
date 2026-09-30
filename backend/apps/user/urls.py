from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import RegisterView, LoginView, UserProfileView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='user-register'),
    path('login/', LoginView.as_view(), name='user-login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
]