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
from webpage.models import *
from webpage.forms import SessionForm
import logging
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.db.models import Count, OuterRef, Subquery, Avg, Q, Sum
from django.contrib.auth.models import User
from typing import Iterable

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
    user_count = UserInfo.objects.count()
    enrollment_count = Transaction.objects.filter(status='enrolled').count()
    session_count = Session.objects.count()
    context = {
        'user_count': user_count,
        'enrollment_count': enrollment_count,
        'session_count': session_count,
    }
    return render(request, 'investor.html', context)


class StatisticView(generic.TemplateView):
    template_name = 'statistics.html'
    
    def get_popular_tutor_name(self, number: int) -> list[str] | None:
        tutors_with_session_counts = User.objects.annotate(num_courses=Count('session'))

        tutors_with_sessions = tutors_with_session_counts.filter(num_courses__gt=0)
        
        tutors_with_participant_counts = (
            tutors_with_sessions
            .annotate(total_participants=Count('session__participants'))
        )
        
        top_tutor = tutors_with_participant_counts.order_by('-total_participants')[:number]
        if top_tutor:
            return [tutor.username for tutor in top_tutor]
        else:
            return None
        
    def get_popular_course(self, number: int) -> Iterable[Session] | None:
        session_with_participant_counts = (
            Session.objects
            .annotate(total_participants=Count('participants'))
        )
        
        top_sessions = session_with_participant_counts.order_by('-total_participants')[:number]
        if top_sessions:
            return top_sessions
        else:
            return None
        
    def get_popular_category(self, number) -> list[Category] | None:
        category_with_participant_counts = (
            Category.objects
            .annotate(total_participants=Count('session__participants'))
        )
        top_categories = category_with_participant_counts.order_by('-total_participants')[:number]
        if top_categories:
            return [category.category_name for category in top_categories]
        else:
            return None
        
    def get_top_5_of_each_category(self):
        # Step 1: Annotate tutors with participant counts per category
        tutors_with_session_counts = User.objects.annotate(num_courses=Count('session'))
        tutors_with_sessions = tutors_with_session_counts.filter(num_courses__gt=0)
        tutors_with_participant_counts = (
            tutors_with_sessions
            .annotate(total_participants=Count('session__participants'))
        )

        # Step 2: Get top 5 tutors for each category
        top_tutors_per_category = {}

        for category in Category.objects.all():
            # Filter tutors who have sessions in the current category
            tutors = (
                tutors_with_participant_counts
                .filter(session__category=category)
                .order_by('-total_participants')[:5]  # Get top 5 tutors
            )

            top_tutors_per_category[category.category_name] = list(tutors)

        return top_tutors_per_category

    def get_avg_enrollment_per_user(self) -> float:
        average = User.objects.annotate(num_enroll=Count("joined_sessions")).aggregate(Avg("num_enroll"))
        return average['num_enroll__avg']
    
    def get_avg_courses_per_tutor(self) -> float:
        tutors_with_session_counts = User.objects.annotate(num_courses=Count('session'))

        tutors_with_sessions = tutors_with_session_counts.filter(num_courses__gt=0)

        average = tutors_with_sessions.aggregate(Avg('num_courses'))    
        return average['num_courses__avg']
    
    def get_catagory_with_most_revenue(self):
        category_with_participant_counts = (
            Category.objects
            .annotate(total_money=Sum('session__transaction__fee'))
        )
        top_categories = category_with_participant_counts.order_by('-total_money').first()
        
        return top_categories
        
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        NUMBER_OF_POPULAR_TUTORS = 5    
        context =  super().get_context_data(**kwargs)
        context["popular_tutors"] = self.get_popular_tutor_name(NUMBER_OF_POPULAR_TUTORS)
        context["popular_sessions"] = self.get_popular_course(NUMBER_OF_POPULAR_TUTORS)
        context['popular_categories'] = self.get_popular_category(NUMBER_OF_POPULAR_TUTORS)
        context['popular_per_category'] = self.get_top_5_of_each_category()
        context['avg_num_enroll'] = self.get_avg_enrollment_per_user()
        context['avg_course_per_tutor'] = self.get_avg_courses_per_tutor()
        context['ctg_with_most_rev'] = self.get_catagory_with_most_revenue()

        return context


def apply_session(request, pk):
    session = get_object_or_404(Session, pk=pk)
    current_datetime = timezone.now()
    payment_id = request.POST.get('payment_id', '')
    try:
        transaction = Transaction.objects.get(session=session,
                                              learner=request.user,
                                              status='cancelled')
        transaction.date = current_datetime.date()
        transaction.time = current_datetime.time()
        transaction.status = 'pending'
        transaction.payment_id = payment_id
        transaction.save()
    except Transaction.DoesNotExist:
        transaction = Transaction(
            session=session,
            learner=request.user,
            tutor=session.tutor_id,
            date=current_datetime.date(),
            time=current_datetime.time(),
            fee=session.fee,
            payment_id=payment_id,
            status='pending'
        )
        transaction.save()
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
    return redirect('session-detail', pk=session_id)


def cancel_session(request, session_id, applicant_id):
    session = get_object_or_404(Session, pk=session_id)
    applicant = get_object_or_404(User, pk=applicant_id)
    transaction = Transaction.objects.get(session=session,
                                          learner=applicant,
                                          status='pending')
    transaction.status = 'cancelled'
    transaction.save()
    return redirect('session-detail', pk=session_id)


def leave_session(request, pk):
    session = get_object_or_404(Session, pk=pk)
    transaction = Transaction.objects.get(session=session,
                                          learner=request.user,
                                          status='enrolled')
    transaction.status = 'left'
    transaction.save()
    session.participants.remove(request.user)
    return redirect('session-detail', pk=pk)
