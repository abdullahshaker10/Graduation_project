from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

JOBS_CHOICES =[
    ('Doctor', 'Doctor'),
    ('Egineer', 'Egineer'),
    ('Radiologist', 'Radiologist'),

]
class SignUpForm(UserCreationForm):
    specialty = forms.CharField(max_length = 200, widget=forms.Select(choices=JOBS_CHOICES))
    Email = forms.EmailField()


    class Meta(UserCreationForm.Meta):
      model = User
      fields =('username','Email','password1','password2','specialty')
      help_texts = {
            'username': None,
            'email': None,
            'password1': None,
            'password2': None,
            'specialty': None,
        }
