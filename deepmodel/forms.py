from django import forms


class SlicesForm(forms.Form):
    slice_num = forms.CharField()
    patient_id = forms.CharField()


class SlicesFormdl(forms.Form):
    slice_num = forms.CharField()
    patient_id = forms.CharField()
