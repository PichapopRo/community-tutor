from django.urls import path

from . import views
from .views import SessionCreateView, SessionDetailView

urlpatterns = [
    path("", views.SessionView.as_view(), name="session-list"),
    path('session/<int:pk>/apply/', views.apply_session, name='apply-session'),
    path('session/<int:session_id>/<int:applicant_id>/accept/', views.accept_session, name='accept-session'),
    path('session/<int:session_id>/<int:applicant_id>/cancel/', views.cancel_session, name='cancel-session'),
    path('session/<int:pk>/leave/', views.leave_session, name='leave-session'),
    path("session/<int:pk>/", SessionDetailView.as_view(), name="session-detail"),
    path('create/', SessionCreateView.as_view(), name='session-create'),
    path("investor", views.investor, name="investor"),
    path("statistics", views.statistics, name="statistics")
]