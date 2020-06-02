from django import forms

# Custom App
from .models import (
    Job,
    Category,
    JobTracking,
)


class JobTrackingForm(forms.ModelForm):
    class Meta:
        model = JobTracking
        fields = ['job', 'seeker_id', 'seeker_name']





