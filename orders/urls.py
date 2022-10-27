from django.urls import path
from . import views

urlpatterns = [
    path("", views.OrdersView.as_view()),
    path("<int:pk>", views.OrderView.as_view()),
]
