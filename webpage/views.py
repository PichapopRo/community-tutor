from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic


def index(request):
    return render(request, 'index.html')


def investor(request):
    return render(request, 'investor.html')


def statistics(request):
    return render(request, 'statistics.html')
