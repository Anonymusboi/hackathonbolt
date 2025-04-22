# backend/admin.py
from django.contrib import admin
from .models import Profile, JobSeeker, Employer, JobListing, Application

# This class customizes the admin interface for JobSeeker model.
class JobSeekerAdmin(admin.ModelAdmin):
    list_display = ('user', 'ready_to_work', 'anonymous_profile')
    search_fields = ('user__username', 'user__email', 'skills')

# This class customizes the admin interface for Employer model.
class EmployerAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'user', 'is_felony_friendly')
    search_fields = ('company_name', 'user__username')

# This class customizes the admin interface for JobListing model.
class JobListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'employer', 'location', 'is_felony_ok', 'created_at')
    list_filter = ('is_felony_ok', 'job_type')
    search_fields = ('title', 'description', 'skills_required')

# This class customizes the admin interface for Application model.
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('job', 'applicant', 'status', 'applied_at')
    list_filter = ('status', 'is_anonymous')
    search_fields = ('job__title', 'applicant__user__username')

admin.site.register(Profile)
admin.site.register(JobSeeker, JobSeekerAdmin)
admin.site.register(Employer, EmployerAdmin)
admin.site.register(JobListing, JobListingAdmin)
admin.site.register(Application, ApplicationAdmin)