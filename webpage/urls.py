from django.urls import path

from . import views
from .views import SessionCreateView

urlpatterns = [
    path("", views.SessionView.as_view(), name="session-list"),
    path('create/', SessionCreateView.as_view(), name='session-create'),
    path("investor", views.investor, name="investor"),
    path("statistics", views.statistics, name="statistics")
]