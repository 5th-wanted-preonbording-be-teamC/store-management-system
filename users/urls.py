from django.urls import path
from users import views

urlpatterns = [
    path("", views.RegisterAPIView.as_view()),
    path("<int:pk>/", views.UserDetailAPIView.as_view()),
]