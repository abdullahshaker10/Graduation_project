from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from basicapp.models import Employee, Patient
from basicapp.forms import EmployeeForm, PatientForm
from django.urls import reverse_lazy
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import (TemplateView, FormView, ListView,
                                  DetailView, CreateView, UpdateView, DeleteView)
from django.shortcuts import render, get_object_or_404

# Create your views here.


def patient_list(request):
    patients = Patient.objects.all()
    return render(request, 'patient_list.html', {'patients': patients})


def upload(request):
    context = {}
    if request.method == 'POST':
        form = PatientForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/basicapp/patient_list/')

    else:
        form = PatientForm()
    return render(request, 'patient_form.html', {'form': form})


class AboutView(TemplateView):
    template_name = 'about.html'


class IndexView(TemplateView):
    template_name = 'index.html'
