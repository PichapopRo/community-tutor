from django.urls import path

from . import views
from .views import SessionCreateView, SessionDetailView

urlpatterns = [
    path("", views.SessionView.as_view(), name="session-list"),
    path('session/<int:pk>/join/', views.join_session, name='join-session'),
    path('session/<int:pk>/leave/', views.leave_session, name='leave-session'),
    path("session/<int:pk>/", SessionDetailView.as_view(), name="session-detail"),
    path('create/', SessionCreateView.as_view(), name='session-create'),
    path("investor/", views.investor, name="investor"),
    path("statistics", views.statistics, name="statistics")
]