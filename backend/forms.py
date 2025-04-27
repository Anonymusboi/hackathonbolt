# backend/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import JobSeeker, Employer, JobListing, Application

class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User  # This form is based on Django's built-in User model.
        fields = ['username', 'email', 'password1', 'password2']  # Fields to show in the form.


class ProfileTypeForm(forms.Form):
    PROFILE_CHOICES = (
        ('job_seeker', 'I am looking for a job'),  # Option for job seekers.
        ('employer', 'I want to hire formerly incarcerated individuals'),  # Option for employers.
    )
    profile_type = forms.ChoiceField(choices=PROFILE_CHOICES, widget=forms.RadioSelect)  # Use radio buttons.


class JobSeekerProfileForm(forms.ModelForm):
    class Meta:
        model = JobSeeker  # Based on the JobSeeker model.
        fields = ['skills', 'experience', 'certifications', 'ready_to_work', 'anonymous_profile', 'resume']
        # These are the fields from JobSeeker that will appear in the form.


class EmployerProfileForm(forms.ModelForm):
    class Meta:
        model = Employer  # Based on the Employer model.
        fields = ['company_name', 'description', 'is_felony_friendly', 'website', 'logo']
        # Form fields correspond to attributes of an Employer.


class JobListingForm(forms.ModelForm):
    class Meta:
        model = JobListing  # Based on the JobListing model.
        fields = ['title', 'description', 'location', 'skills_required', 'is_felony_ok', 
                 'expires_at', 'salary_range', 'job_type']  # Job listing fields to display.
        widgets = {
            'expires_at': forms.DateInput(attrs={'type': 'date'}),  # Use HTML5 date picker for expiration.
        }
        
class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application  # Based on the Application model.
        fields = ['cover_letter', 'is_anonymous']  # Fields shown to applicants.
