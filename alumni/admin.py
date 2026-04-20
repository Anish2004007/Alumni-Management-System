from django.contrib import admin
from django.utils.html import format_html
from .models import Alumni, JobOpportunity, JobApplication, Event, Donation

@admin.register(Alumni)
class AlumniAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'student_id', 'degree', 'major', 'graduation_year', 'is_approved', 'created_at']
    list_filter = ['is_approved', 'degree', 'graduation_year']
    list_editable = ['is_approved']
    search_fields = ['user__first_name', 'user__last_name', 'student_id', 'major', 'company']
    readonly_fields = ['created_at', 'updated_at']
    actions = ['approve_alumni', 'reject_alumni']

    def full_name(self, obj):
        return obj.user.get_full_name() or obj.user.username
    full_name.short_description = 'Name'

    def approve_alumni(self, request, queryset):
        count = queryset.update(is_approved=True)
        self.message_user(request, f'✅ {count} alumni approved successfully.')
    approve_alumni.short_description = '✅ Approve selected alumni'

    def reject_alumni(self, request, queryset):
        count = queryset.update(is_approved=False)
        self.message_user(request, f'❌ {count} alumni rejected.')
    reject_alumni.short_description = '❌ Reject selected alumni'

    fieldsets = (
        ('Personal Info', {
            'fields': ('user', 'student_id', 'phone', 'address', 'photo')
        }),
        ('Academic Info', {
            'fields': ('degree', 'major', 'graduation_year')
        }),
        ('Professional Info', {
            'fields': ('current_job', 'company', 'email', 'linkedin', 'bio')
        }),
        ('Status', {
            'fields': ('is_approved', 'registration_fee_paid', 'training_completed', 'donation_amount')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(JobOpportunity)
class JobOpportunityAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'location', 'job_type', 'salary', 'application_deadline', 'is_active', 'applications_count']
    list_filter = ['is_active', 'job_type']
    list_editable = ['is_active']
    search_fields = ['title', 'company', 'location']
    readonly_fields = ['posted_date']
    actions = ['activate_jobs', 'deactivate_jobs']

    def applications_count(self, obj):
        count = obj.applications.count()
        return format_html('<b>{}</b> applications', count)
    applications_count.short_description = 'Applications'

    def activate_jobs(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, 'Jobs activated.')
    activate_jobs.short_description = '✅ Activate selected jobs'

    def deactivate_jobs(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, 'Jobs deactivated.')
    deactivate_jobs.short_description = '❌ Deactivate selected jobs'

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ['applicant_name', 'job_title', 'company', 'status', 'applied_date']
    list_filter = ['status', 'applied_date']
    list_editable = ['status']
    search_fields = ['applicant__first_name', 'applicant__last_name', 'job__title', 'job__company']
    readonly_fields = ['applied_date', 'updated_date']
    actions = ['shortlist', 'schedule_interview', 'send_offer', 'reject']

    def applicant_name(self, obj):
        return obj.applicant.get_full_name() or obj.applicant.username
    applicant_name.short_description = 'Applicant'

    def job_title(self, obj):
        return obj.job.title
    job_title.short_description = 'Job'

    def company(self, obj):
        return obj.job.company
    company.short_description = 'Company'

    def shortlist(self, request, queryset):
        queryset.update(status='shortlisted')
        self.message_user(request, f'{queryset.count()} applicants shortlisted.')
    shortlist.short_description = '⭐ Shortlist selected'

    def schedule_interview(self, request, queryset):
        queryset.update(status='interview')
        self.message_user(request, f'{queryset.count()} interviews scheduled.')
    schedule_interview.short_description = '📅 Schedule interview'

    def send_offer(self, request, queryset):
        queryset.update(status='offered')
        self.message_user(request, f'{queryset.count()} offers sent.')
    send_offer.short_description = '🎉 Send offer'

    def reject(self, request, queryset):
        queryset.update(status='rejected')
        self.message_user(request, f'{queryset.count()} applications rejected.')
    reject.short_description = '❌ Reject selected'

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'date', 'location', 'registration_fee', 'max_participants', 'organizer']
    list_filter = ['date']
    search_fields = ['title', 'location']
    readonly_fields = ['created_at']

@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ['alumni', 'amount', 'purpose', 'donation_date', 'is_recurring']
    list_filter = ['is_recurring', 'donation_date']
    search_fields = ['alumni__user__first_name', 'alumni__user__last_name']
    readonly_fields = ['donation_date']