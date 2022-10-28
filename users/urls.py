from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from users import views

urlpatterns = [
    path("", views.RegisterAPIView.as_view()),
    path("<int:pk>/", views.UserDetailAPIView.as_view()),
]
