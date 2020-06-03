from django import forms

# Custom App
from .models import (
    Job,
    Category,
    JobTracking,
)


# Category Form
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']


# Job Form
class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = '__all__'


# JobTracking Form
class JobTrackingForm(forms.ModelForm):
    class Meta:
        model = JobTracking
        fields = ['job', 'seeker_id', 'seeker_name']







