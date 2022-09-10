from django import forms

SPECIALITY_TYPE=(
    ("ear","ear"),
    ("eye","eye"),
    ("cardiology","cardiology"),
)

class AvailabilityForm(forms.Form):

#    hid = forms.CharField(widget=forms.HiddenInput)
    speciality = forms.ChoiceField(choices = SPECIALITY_TYPE, required=True)
    doctor = forms.CharField(max_length=100,required=True)
    start_datetime = forms.DateTimeField(required=True, input_formats=["%Y"])
    end_datetime = forms.DateTimeField(required=True, input_formats=["%Y"])
    pat_name = forms.CharField(max_length=100,required=True)
    pat_address = forms.CharField(max_length=100,required=True)
    pat_contact = forms.IntegerField(required=True)
    
