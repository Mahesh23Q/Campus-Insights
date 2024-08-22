from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegForm, ExamForm, QuestionForm
from django.core.mail import send_mail
from Campus_Insight import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import datetime
from .models import Exam, Question  # Ensure you have an Exam model
from docx import Document
from django.http import JsonResponse, HttpResponseRedirect
import json
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods, require_POST
from django.urls import reverse
import logging

def home(request):
    return render(request,"index.html")

@login_required
def gallery(request):
    return render(request,"gallery.html")

@login_required
def events(request):
    return render(request,"events.html")

@login_required
def activities(request):
    return render(request,"activities.html")

@login_required
def profile(request):
    return render(request,"profile.html")

@login_required
def dashboard(request):
    exams = Exam.objects.all()  # Fetch all exams from the database
    if request.user.user_role == 'F':
        return render(request,"Fdashboard.html",{'exams': exams})
    else:
        return render(request,"dashboard.html")

def register(request):
	if request.method == "POST":
		p = RegForm(request.POST)
		if p.is_valid():
			v = p.save(commit=False)
			s = send_mail("S-Mart Registration","Thanks for Subscribing to this site",settings.EMAIL_HOST_USER,[v.email]) 
			if s == 1:
				v.save()
				messages.success(request,"Registered Successfully please check your mail for confirmation")
				return redirect('/login/')
			else:
				messages.warning(request,"Not registered please enter Your correct mailid")
				return redirect('/register/')
	else:
		p = RegForm()
	return render(request,'register.html',{'z':p})

def about(request):
    return render(request,"about.html")

def terms(request):
    return render(request,"terms.html")

def contact(request):
    return render(request,"contact.html")
