from django import forms
from basicapp.models import Employee, Patient


class EmployeeForm(forms.ModelForm):

    class Meta():
        model = Employee
        fields = '__all__'


class PatientForm(forms.ModelForm):

    class Meta():
        model = Patient
        fields = ['name', 'PATIENT_DICOM',]
