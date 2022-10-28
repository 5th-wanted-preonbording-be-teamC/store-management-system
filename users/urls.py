from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from users import views

urlpatterns = [
    path("", views.RegisterAPIView.as_view()),
    path("<int:pk>/", views.UserDetailAPIView.as_view()),
    path("api-token-auth/", obtain_auth_token),
]