from django.shortcuts import render, redirect, get_object_or_404
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
    success_url = '/'

    def form_valid(self, form):
        print("Form is valid!")
        return super().form_valid(form)

    def form_invalid(self, form):
        print("Form is invalid!")
        print(form.errors)
        return self.render_to_response(self.get_context_data(form=form))


class SessionDetailView(generic.DetailView):
    model = Session
    template_name = 'session_detail.html'
    context_object_name = 'session'

    def get_object(self, queryset=None):
        session_id = self.kwargs.get('pk')
        return get_object_or_404(Session, pk=session_id)


def investor(request):
    return render(request, 'investor.html')


def statistics(request):
    return render(request, 'statistics.html')
