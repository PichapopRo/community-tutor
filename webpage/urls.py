from django.urls import path

from . import views

urlpatterns = [
    path("", views.AvailableCoursesView.as_view(), name="course-list"),
    path("create/", views.CourseCreateView.as_view(), name='course-create')
]