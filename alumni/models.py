# alumni/models.py
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Alumni(models.Model):
    GRADUATION_YEAR_CHOICES = [(r, r) for r in range(2000, 2031)]
    DEGREE_CHOICES = [
        ('Bachelors', 'Bachelors'),
        ('Masters', 'Masters'),
        ('PhD', 'PhD'),
        ('Diploma', 'Diploma'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=20, unique=True)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    graduation_year = models.IntegerField(choices=GRADUATION_YEAR_CHOICES)
    degree = models.CharField(max_length=20, choices=DEGREE_CHOICES)
    major = models.CharField(max_length=100)
    current_job = models.CharField(max_length=200, blank=True)
    company = models.CharField(max_length=200, blank=True)
    email = models.EmailField()
    linkedin = models.URLField(blank=True)
    photo = models.ImageField(upload_to='alumni_photos/', blank=True, null=True)
    bio = models.TextField(blank=True)
    registration_fee_paid = models.BooleanField(default=False)
    training_completed = models.BooleanField(default=False)
    donation_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.student_id}"

    def get_absolute_url(self):
        return reverse('alumni_detail', kwargs={'pk': self.pk})

class JobOpportunity(models.Model):
    JOB_TYPE_CHOICES = [
        ('Full-time', 'Full-time'),
        ('Part-time', 'Part-time'),
        ('Internship', 'Internship'),
        ('Contract', 'Contract'),
    ]
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=100)
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES)
    salary = models.CharField(max_length=100, blank=True)
    requirements = models.TextField()
    contact_email = models.EmailField()
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    posted_date = models.DateTimeField(auto_now_add=True)
    application_deadline = models.DateField()

    def __str__(self):
        return f"{self.title} at {self.company}"

class JobApplication(models.Model):
    STATUS_CHOICES = [
        ('applied', 'Applied'),
        ('under_review', 'Under Review'),
        ('shortlisted', 'Shortlisted'),
        ('interview', 'Interview Scheduled'),
        ('offered', 'Offer Received'),
        ('rejected', 'Rejected'),
        ('withdrawn', 'Withdrawn'),
    ]
    job = models.ForeignKey(JobOpportunity, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='job_applications')
    cover_letter = models.TextField()
    resume_link = models.URLField(blank=True, help_text='Link to your resume (Google Drive, LinkedIn, etc.)')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='applied')
    applied_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True)

    class Meta:
        unique_together = ('job', 'applicant')

    def __str__(self):
        return f"{self.applicant.get_full_name()} → {self.job.title}"

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=200)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE)
    registration_fee = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    max_participants = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Donation(models.Model):
    alumni = models.ForeignKey(Alumni, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    donation_date = models.DateTimeField(auto_now_add=True)
    purpose = models.CharField(max_length=200, blank=True)
    is_recurring = models.BooleanField(default=False)

    def __str__(self):
        return f"Donation from {self.alumni.user.get_full_name()}"