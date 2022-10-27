from django.urls import path
from . import views

urlpatterns = [
    path("", views.Payments.as_view()),
    path("<int:pk>/", views.Payment.as_view()),
]
