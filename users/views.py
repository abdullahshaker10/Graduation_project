from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import SignUpForm

# Create your views here.


def resgister(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your Account Has been Created You Are Now Able To Login')
            return redirect('login')

    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})
