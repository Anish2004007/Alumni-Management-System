# alumni/admin.py
from django.contrib import admin
from alumni.models import Alumni, JobOpportunity, Event, Donation

@admin.register(Alumni)
class AlumniAdmin(admin.ModelAdmin):
    list_display = ['user', 'student_id', 'graduation_year', 'degree', 'is_approved']
    list_filter = ['graduation_year', 'degree', 'is_approved']
    search_fields = ['user__first_name', 'user__last_name', 'student_id']
    list_editable = ['is_approved']

@admin.register(JobOpportunity)
class JobOpportunityAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'job_type', 'is_active', 'posted_date']
    list_filter = ['job_type', 'is_active']
    search_fields = ['title', 'company']

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'date', 'location', 'organizer']
    list_filter = ['date']

@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ['alumni', 'amount', 'donation_date']
    list_filter = ['donation_date']