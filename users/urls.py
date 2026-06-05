from django.urls import path, include
from .views import RegisterView, MeView
from .token_views import EmailTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', EmailTokenObtainPairView.as_view(), name='login'),
    path('me/', MeView.as_view(), name='me'), 
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path(
    'password_reset/',
    include('django_rest_passwordreset.urls', namespace='password_reset')
),
]
