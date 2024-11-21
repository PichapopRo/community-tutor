from django.views.generic import ListView
from webpage.models import Course
from .forms import CourseForm
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy


class AvailableCoursesView(ListView):
    model = Course
    template_name = 'courses/available_courses.html'
    context_object_name = 'courses'

    def get_queryset(self):
        return Course.objects.all().order_by('course_name')


class CourseCreateView(CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'courses/course_form.html'
    success_url = reverse_lazy(
        'available_courses')
