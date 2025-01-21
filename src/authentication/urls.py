from django.urls import path

from authentication.api import UserLoginAPIView, UserLogoutAPIView

urlpatterns = [
    path("login/", UserLoginAPIView.as_view(), name='login'),
    path("logout/", UserLogoutAPIView.as_view(), name="logout")
]
