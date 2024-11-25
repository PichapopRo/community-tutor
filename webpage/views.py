from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import generic

from webpage.forms import SessionForm
from webpage.models import Session


class SessionView(generic.ListView):
    model = Session
    context_object_name = 'sessions'
    template_name = 'session_list.html'

    def get_queryset(self):
        all_sessions = Session.objects.all()
        return [session for session in all_sessions if session.can_apply()]


class SessionCreateView(generic.CreateView):
    model = Session
    template_name = 'session_form.html'
    form_class = SessionForm

    def form_valid(self, form):
        print("Form is valid!")
        return super().form_valid(form), redirect(reverse('session_list'))

    def form_invalid(self, form):
        print("Form is invalid!")
        print(form.errors)
        return self.render_to_response(self.get_context_data(form=form))

def investor(request):
    return render(request, 'investor.html')


def statistics(request):
    return render(request, 'statistics.html')
