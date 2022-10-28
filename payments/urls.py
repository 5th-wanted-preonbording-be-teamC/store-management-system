from typing import Final
from django.urls import path
from . import views

urlpatterns: Final = [
    path("", views.PaymentListView.as_view()),
    path("<int:pk>/", views.PaymentView.as_view()),
]
