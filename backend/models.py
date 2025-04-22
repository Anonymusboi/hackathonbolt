from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Profile model extends the default User model with additional fields
class Profile(models.Model):
    # User type choices - determines if user is job seeker or employer
    USER_TYPES = (
        ('job_seeker', 'Job Seeker'),
        ('employer', 'Employer'),
    )
    # One-to-one relationship with Django's built-in User model
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=20, choices=USER_TYPES)
    phone = models.CharField(max_length=20, blank=True)  # Optional phone number
    address = models.TextField(blank=True)  # Optional address
    
    def __str__(self):
        return f"{self.user.username}'s Profile"

# Model for job seekers with specific fields relevant to their situation
class JobSeeker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='job_seeker')
    skills = models.TextField(help_text="List your skills separated by commas")
    experience = models.TextField(blank=True)  # Work history can be left blank
    certifications = models.TextField(blank=True)  # Any professional certifications
    ready_to_work = models.BooleanField(default=False)  # Availability status
    anonymous_profile = models.BooleanField(default=False)  # Privacy option
    success_story = models.TextField(blank=True)  # Optional success narrative
    resume = models.FileField(upload_to='resumes/', blank=True)  # Upload resume
    
    def __str__(self):
        return f"{self.user.get_full_name()} (Job Seeker)"

# Model for employers who want to hire formerly incarcerated individuals
class Employer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255)
    description = models.TextField()  # Company overview
    is_felony_friendly = models.BooleanField(default=False)  # Explicit felony-friendly status
    website = models.URLField(blank=True)  # Optional company website
    logo = models.ImageField(upload_to='employer_logos/', blank=True)  # Company logo
    
    def __str__(self):
        return f"{self.company_name} (Employer)"

# Model for job listings posted by employers
class JobListing(models.Model):
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)  # Job title
    description = models.TextField()  # Detailed job description
    location = models.CharField(max_length=255)  # Job location
    skills_required = models.TextField()  # Required skills
    is_felony_ok = models.BooleanField(default=False)  # Explicitly felony-friendly position
    created_at = models.DateTimeField(auto_now_add=True)  # Auto-set when created
    expires_at = models.DateTimeField()  # Job posting expiration date
    salary_range = models.CharField(max_length=100, blank=True)  # Optional salary info
    # Job type choices
    job_type = models.CharField(max_length=50, choices=[
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('contract', 'Contract'),
        ('temporary', 'Temporary'),
    ])
    
    def __str__(self):
        return f"{self.title} at {self.employer.company_name}"

# Model for tracking job applications
class Application(models.Model):
    job = models.ForeignKey(JobListing, on_delete=models.CASCADE)
    applicant = models.ForeignKey(JobSeeker, on_delete=models.CASCADE)
    applied_at = models.DateTimeField(auto_now_add=True)  # Auto-set application date
    # Application status choices
    status = models.CharField(max_length=50, choices=[
        ('applied', 'Applied'),
        ('reviewed', 'Reviewed'),
        ('interview', 'Interview Scheduled'),
        ('hired', 'Hired'),
        ('rejected', 'Rejected')
    ], default='applied')
    is_anonymous = models.BooleanField(default=False)  # Privacy option
    cover_letter = models.TextField(blank=True)  # Optional cover letter
    
    def __str__(self):
        return f"{self.applicant.user.get_full_name()} applied for {self.job.title}"

# Signal to create a Profile whenever a User is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# Signal to save the Profile whenever the User is saved
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()