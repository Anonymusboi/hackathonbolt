from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import JobSeeker, Employer, JobListing, Application, Profile
from .forms import (UserRegisterForm, ProfileTypeForm, JobSeekerProfileForm, 
                   EmployerProfileForm, JobListingForm, ApplicationForm)
from .matching import JobMatcher

def home(request):
    return render(request, 'home.html')

# Handle user registration
def register(request):
    if request.method == "POST":  # Check if form was submitted
        form = UserRegisterForm(request.POST)  # Populate form with POST data
        if form.is_valid():  # Validate form input
            form.save()  # Create a new user
            username = form.cleaned_data.get('username')  # Get the username
            messages.success(request, f'Account created for {username}! Please complete your profile.') 
            return redirect('login') 
    else:
        form = UserRegisterForm()  # Display empty registration form
    return render(request, 'registration/register.html', {'form': form})  # Render registration template with form


# Handle choosing a profile type (Job Seeker or Employer)
@login_required
def profile_type(request):
    if hasattr(request.user,'employer') or hasattr(request.user, 'job_seeker'):  # Redirect if user already has a choice made
        return redirect('dashboard')    

    if request.method == "POST": 
        form = ProfileTypeForm(request.POST)  
        if form.is_valid(): 
            profile_type = form.cleaned_data['profile_type']  # Get selected type (job_seeker or employer)
            request.user.profile.user_type = profile_type  # Save type to profile
            request.user.profile.save()  # Save profile instance

            if profile_type == 'job_seeker':  
                # Check if JobSeeker already exists
                if not hasattr(request.user, 'job_seeker'):
                    JobSeeker.objects.create(user=request.user)  
                return redirect('jobseeker_profile')  
            else:
                # Check if Employer already exists
                if not hasattr(request.user, 'employer'):
                    Employer.objects.create(user=request.user)  
                return redirect('employer_profile')  
    else:
        form = ProfileTypeForm()  # Create empty form if not POST
    return render(request, 'profile_type.html', {'form': form})  # Render form for selecting profile type


# Handle Job Seeker profile form
@login_required
def job_seeker_profile(request):
    # if hasattr(request.user, 'employer'):  # Block employers from accessing this view
    #    return redirect('dashboard')

    job_seeker = request.user.job_seeker  # Get the current job seeker's profile
    if request.method == "POST": 
        form = JobSeekerProfileForm(request.POST, request.FILES, instance=job_seeker)  # Bind form to existing instance and data
        if form.is_valid():  
            form.save()  
            messages.success(request, 'Profile updated successfully!') 
            return redirect('jobseeker_dashboard')  
    else:
        form = JobSeekerProfileForm()
    return render(request, 'jobseeker_profile.html', {'form': form})  

# Handle Employer profile form
@login_required
def employer_profile(request):
    if hasattr(request.user, 'job_seeker'):  # Block job seekers from accessing this view
        return redirect('dashboard')

    employer = request.user.employer  # Get the current employer's profile
    if request.method == "POST":  
        form = EmployerProfileForm(request.POST, request.FILES, instance=employer)  
        if form.is_valid(): 
            form.save()  
            messages.success(request, 'Profile updated successfully!') 
            return redirect('employer_dashboard')  
    else:
        form = EmployerProfileForm(instance=employer)  
    return render(request, 'employer_profile.html', {'form': form})  

# Redirect users to the appropriate dashboard based on their role
@login_required
def dashboard(request):
    if hasattr(request.user, 'job_seeker'):  
        return redirect('jobseeker_dashboard')
    elif hasattr(request.user, 'employer'):  
        return redirect('employer_dashboard')
    return redirect('profile_type')  

# Job Seeker dashboard showing matched jobs
@login_required
def job_seeker_dashboard(request):
    if not hasattr(request.user, 'job_seeker'):  # Ensure only job seekers can access
        return redirect('profile_type')

    job_seeker = request.user.job_seeker  
    matcher = JobMatcher()
    all_jobs = JobListing.objects.filter(is_felony_ok=True)  # Get only felony-friendly jobs
    if(all_jobs.count() == 0):  # Check if there are any jobs available:
        messages.warning(request, 'No jobs available at the moment. Please check back later.')  
        matched_jobs = []  # No jobs to match
    else:
        matched_jobs = matcher.match_jobs_to_seeker(job_seeker, all_jobs)  # Find best matches for job seeker

    context = {
        'job_seeker': job_seeker,  # Pass job seeker data
        'matched_jobs': matched_jobs,  # Pass matched jobs
    }
    return render(request, 'job_seeker_dashboard.html', context)  


# Employer dashboard showing job listings and received applications
@login_required
def employer_dashboard(request):
    if not hasattr(request.user, 'employer'):  # Only employers allowed
        return redirect('profile_type')

    employer = request.user.employer  # Get employer profile
    job_listings = JobListing.objects.filter(employer=employer) 
    applications = Application.objects.filter(job__in=job_listings)  

    context = {
        'employer': employer,  # Employer data
        'job_listings': job_listings,  # Their posted jobs
        'applications': applications,  # Applications received
    }
    return render(request, 'employer_dashboard.html', context)  

# View for employers to post a new job
@login_required
def post_job(request):
    if not hasattr(request.user, 'employer'):  
        return redirect('profile_type')
    if request.method == "POST":  
        form = JobListingForm(request.POST)  
        if form.is_valid():  
            job_listing = form.save(commit=False)  # Create but don't save yet
            job_listing.employer = request.user.employer  # Assign current employer to the job
            job_listing.save()  # Save the job listing
            messages.success(request, 'Job listing created successfully!')  
            return redirect('employer_dashboard')  
    else:
        form = JobListingForm()  # Show empty form
    return render(request, 'post_job.html', {'form': form}) 

# View for job seekers to apply to a job
@login_required
def apply_job(request, job_id):
    if not hasattr(request.user, 'job_seeker'):  # Only job seekers can apply
        return redirect('profile_type')

    job = get_object_or_404(JobListing, id=job_id)  # Fetch job or return 404
    job_seeker = request.user.job_seeker  # Get current job seeker

    if Application.objects.filter(job=job, application=job_seeker).exists():  # Check if already applied
        messages.warning(request, 'You have already applied for this job.') 
        return redirect('job_seeker_dashboard')

    if request.method == "POST":  
        form = ApplicationForm(request.POST)  
        if form.is_valid():  
            application = form.save(commit=False)  
            application.job = job  # Assign job
            application.applicant = job_seeker  # Assign applicant
            application.save()  # Save application
            messages.success(request, 'Application submitted successfully!')  
            return redirect('job_seeker_dashboard') 
    else:
        form = ApplicationForm()  # Empty form
    context = {
        'job': job,  # Job data
        'form': form,  # Application form
    }
    return render(request, 'apply_job.html', context)  


# Employer view to see all received applications
@login_required
def view_applications(request):
    if not hasattr(request.user, 'employer'):  # Only employers allowed
        return redirect('profile_type')

    applications = Application.objects.filter(job__employer=request.user.employer)  # Get applications to employer's jobs
    return render(request, 'view_applications.html', {'applications': applications})  # Render list of applications
