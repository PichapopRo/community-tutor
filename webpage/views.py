from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from typing import Any
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import generic
from webpage.forms import UserRegistrationForm, UserInfoForm, SessionForm
from webpage.models import Session, Address, Category, Transaction
from webpage.forms import SessionForm
import logging
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.db.models import Count
from django.contrib.auth.models import User

logger = logging.getLogger("Views.py")


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        user_info_form = UserInfoForm(request.POST)
        logger.debug(user_form.is_valid())
        logger.debug(user_info_form.is_valid())
        if user_form.is_valid() and user_info_form.is_valid():
            user = user_form.save(commit=True)
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            address = Address(
                street_address=user_info_form.cleaned_data['street_address'],
                sub_district=user_info_form.cleaned_data['sub_district'],
                district=user_info_form.cleaned_data['district'],
                province=user_info_form.cleaned_data['province'],
                zip_code=user_info_form.cleaned_data['zip_code']
            )
            address.save()
            user_info = user_info_form.save(commit=False)
            user_info.user = user
            user_info.address = address
            user_info.date_of_birth = user_info_form.cleaned_data[
                'date_of_birth']
            user_info.save()
            login(request, user)
            return redirect('session-list')
    else:
        user_form = UserRegistrationForm()
        user_info_form = UserInfoForm()
    return render(request, 'registration/register.html', {
        'user_form': user_form,
        'user_info_form': user_info_form,
    })


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('session-list')
            else:
                messages.error(request, 'Invalid username or password')
        else:
            messages.error(request, 'Please correct the errors below.')

    else:
        form = AuthenticationForm()

    return render(request, 'registration/login.html', {'form': form})


def signout_view(request):
    logout(request)
    return redirect("session-list")


class SessionView(generic.ListView):
    model = Session
    context_object_name = 'sessions'
    template_name = 'session_list.html'

    def get_queryset(self):
        options = self.request.GET.get("filter_option")
        if options:
            all_sessions = Session.objects.filter(
                category__category_id=options)
        else:
            all_sessions = Session.objects.all()
        return [session for session in all_sessions if session.can_apply()]

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()

        return context


class SessionCreateView(LoginRequiredMixin, generic.CreateView):
    model = Session
    template_name = 'session_form.html'
    form_class = SessionForm
    success_url = '/'

    def form_valid(self, form):
        form.instance.tutor_id = self.request.user
        logger.debug("Form is valid!")
        return super().form_valid(form)

    def form_invalid(self, form):
        logger.debug("Form is invalid!")
        logger.debug(form.errors)
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


class StatisticView(generic.TemplateView):
    template_name = 'statistics.html'
    
    def get_popular_tutor_name(self, number: int) -> list[str] | None:
        tutors_with_participant_counts = (
            User.objects
            .annotate(total_participants=Count('joined_sessions'))
        )
        
        top_tutor = tutors_with_participant_counts.order_by('-total_participants')[:number]
        if top_tutor:
            return [tutor.username for tutor in top_tutor]
        else:
            return None
        
    def get_popular_course_name(self, number: int) -> list[Session] | None:
        session_with_participant_counts = (
            Session.objects
            .annotate(total_participants=Count('participants'))
        )
        
        top_sessions = session_with_participant_counts.order_by('-total_participants')[:number]
        if top_sessions:
            return top_sessions
        else:
            return None
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        NUMBER_OF_POPULAR_TUTORS = 5    
        context =  super().get_context_data(**kwargs)
        context["popular_tutors"] = self.get_popular_tutor_name(NUMBER_OF_POPULAR_TUTORS)
        context["popular_sessions"] = self.get_popular_course_name(NUMBER_OF_POPULAR_TUTORS)
        
        
        return context


def join_session(request, pk):
    session = get_object_or_404(Session, pk=pk)

    if session.is_full():
        messages.error(request, "This session is already full.")
        return redirect('session-detail', pk=pk)

    if request.user in session.participants.all():
        messages.warning(request,
                         "You are already a participant in this session.")
    else:
        current_datetime = timezone.now()
        transaction = Transaction(
            session_id=session,
            learner=request.user,
            tutor=session.tutor_id,
            date=current_datetime.date(),
            time=current_datetime.time(),
            fee=session.fee,
            status='pending'
        )
        transaction.save()
        messages.success(request, "You have successfully applied the session.")
    return redirect('session-detail', pk=pk)


@login_required
def leave_session(request, pk):
    session = get_object_or_404(Session, pk=pk)
    if request.user in session.participants.all():
        session.participants.remove(request.user)
    return redirect('session-detail', pk=pk)
