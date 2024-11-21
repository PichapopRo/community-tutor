from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("investor", views.investor, name="investor"),
    path("statistics", views.statistics, name="statistics")
]