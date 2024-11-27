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


def statistics(request):
    return render(request, 'statistics.html')


def apply_session(request, pk):
    session = get_object_or_404(Session, pk=pk)
    if Transaction.objects.filter(session=session,
                                  learner=request.user,
                                  status='cancelled').first():
        transaction = Transaction.objects.get(session=session,
                                              learner=request.user,
                                              status='cancelled')
        transaction.status = 'pending'
        transaction.save()
    else:
        current_datetime = timezone.now()
        transaction = Transaction(
            session=session,
            learner=request.user,
            tutor=session.tutor_id,
            date=current_datetime.date(),
            time=current_datetime.time(),
            fee=session.fee,
            status='pending'
        )
        transaction.save()
    messages.success(request, f"You have successfully applied "
                              f"into {session.session_name}.")
    return redirect('session-detail', pk=pk)


def accept_session(request, session_id, applicant_id):
    session = get_object_or_404(Session, pk=session_id)
    applicant = get_object_or_404(User, pk=applicant_id)
    transaction = Transaction.objects.get(session=session,
                                          learner=applicant,
                                          status='pending')
    transaction.status = 'enrolled'
    transaction.save()
    session.participants.add(applicant)
    session.save()
    messages.success(request, f"You have successfully accepted "
                              f"{applicant.username} in {session.session_name}.")
    return redirect('session-detail', pk=session_id)


def cancel_session(request, session_id, applicant_id):
    session = get_object_or_404(Session, pk=session_id)
    applicant = get_object_or_404(User, pk=applicant_id)
    transaction = Transaction.objects.get(session=session,
                                          learner=applicant,
                                          status='pending')
    transaction.status = 'cancelled'
    transaction.save()
    messages.success(request, f"You have successfully cancelled "
                              f"{applicant.username} in {session.session_name}.")
    return redirect('session-detail', pk=session_id)


def leave_session(request, pk):
    session = get_object_or_404(Session, pk=pk)
    transaction = Transaction.objects.get(session=session,
                                          learner=request.user,
                                          status='enrolled')
    transaction.status = 'left'
    transaction.save()
    session.participants.remove(request.user)
    messages.success(request, f"You have successfully left "
                              f"{session.session_name}.")
    return redirect('session-detail', pk=pk)
