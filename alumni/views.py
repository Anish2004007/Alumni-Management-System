import json
import os
import urllib.request
import urllib.error
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from django.http import JsonResponse

from .models import Alumni, JobOpportunity, JobApplication, Event, Donation
from .forms import AlumniForm, JobOpportunityForm, JobApplicationForm, EventForm, DonationForm, SearchForm

# ── HOME ──────────────────────────────────────────────────────────────────────

def home(request):
    total_alumni = Alumni.objects.filter(is_approved=True).count()
    total_jobs = JobOpportunity.objects.filter(is_active=True).count()
    total_events = Event.objects.filter(date__gte=timezone.now()).count()
    return render(request, 'alumni/home.html', {
        'total_alumni': total_alumni,
        'total_jobs': total_jobs,
        'total_events': total_events,
    })

# ── DASHBOARD ─────────────────────────────────────────────────────────────────

@login_required
def dashboard(request):
    try:
        alumni_profile = Alumni.objects.get(user=request.user)
    except Alumni.DoesNotExist:
        alumni_profile = None

    total_alumni = Alumni.objects.filter(is_approved=True).count()
    recent_jobs = JobOpportunity.objects.filter(is_active=True).order_by('-posted_date')[:5]
    upcoming_events = Event.objects.filter(date__gte=timezone.now()).order_by('date')[:5]
    my_applications = JobApplication.objects.filter(applicant=request.user).order_by('-applied_date')[:5]

    context = {
        'alumni_profile': alumni_profile,
        'total_alumni': total_alumni,
        'recent_jobs': recent_jobs,
        'upcoming_events': upcoming_events,
        'my_applications': my_applications,
    }
    return render(request, 'alumni/dashboard.html', context)

# ── ALUMNI ────────────────────────────────────────────────────────────────────

@login_required
def alumni_list(request):
    form = SearchForm(request.GET or None)
    alumni_qs = Alumni.objects.filter(is_approved=True)
    if form.is_valid():
        query = form.cleaned_data.get('query')
        graduation_year = form.cleaned_data.get('graduation_year')
        degree = form.cleaned_data.get('degree')
        if query:
            alumni_qs = alumni_qs.filter(
                Q(user__first_name__icontains=query) |
                Q(user__last_name__icontains=query) |
                Q(major__icontains=query) |
                Q(current_job__icontains=query) |
                Q(company__icontains=query)
            )
        if graduation_year:
            alumni_qs = alumni_qs.filter(graduation_year=graduation_year)
        if degree:
            alumni_qs = alumni_qs.filter(degree=degree)
    return render(request, 'alumni/alumni_list.html', {'alumni_list': alumni_qs, 'form': form})

@login_required
def alumni_detail(request, pk):
    alumni = get_object_or_404(Alumni, pk=pk, is_approved=True)
    return render(request, 'alumni/alumni_detail.html', {'alumni': alumni})

@login_required
def alumni_create(request):
    # Check if profile already exists
    if Alumni.objects.filter(user=request.user).exists():
        messages.warning(request, 'You already have a profile.')
        return redirect('dashboard')
    if request.method == 'POST':
        form = AlumniForm(request.POST, request.FILES)
        if form.is_valid():
            alumni = form.save(commit=False)
            alumni.user = request.user
            alumni.save()
            request.user.first_name = form.cleaned_data['first_name']
            request.user.last_name = form.cleaned_data['last_name']
            request.user.email = form.cleaned_data['email']
            request.user.save()
            messages.success(request, '✅ Profile submitted! Waiting for admin approval.')
            return redirect('dashboard')
    else:
        form = AlumniForm()
    return render(request, 'alumni/alumni_form.html', {'form': form, 'title': 'Create Profile'})

@login_required
def alumni_update(request, pk):
    alumni = get_object_or_404(Alumni, pk=pk, user=request.user)
    if request.method == 'POST':
        form = AlumniForm(request.POST, request.FILES, instance=alumni)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('alumni_detail', pk=alumni.pk)
    else:
        form = AlumniForm(instance=alumni)
    return render(request, 'alumni/alumni_form.html', {'form': form, 'title': 'Update Profile'})

# ── JOBS ──────────────────────────────────────────────────────────────────────

@login_required
def job_list(request):
    jobs = JobOpportunity.objects.filter(is_active=True).order_by('-posted_date')
    applied_ids = list(JobApplication.objects.filter(
        applicant=request.user).values_list('job_id', flat=True))
    return render(request, 'alumni/job_list.html', {'jobs': jobs, 'applied_ids': applied_ids})

@login_required
def job_detail(request, pk):
    job = get_object_or_404(JobOpportunity, pk=pk, is_active=True)
    already_applied = JobApplication.objects.filter(job=job, applicant=request.user).exists()
    return render(request, 'alumni/job_detail.html', {'job': job, 'already_applied': already_applied})

@login_required
def job_apply(request, pk):
    job = get_object_or_404(JobOpportunity, pk=pk, is_active=True)
    if JobApplication.objects.filter(job=job, applicant=request.user).exists():
        messages.warning(request, 'You have already applied for this job.')
        return redirect('job_detail', pk=pk)
    if request.method == 'POST':
        form = JobApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.applicant = request.user
            application.save()
            messages.success(request, f'✅ Successfully applied to {job.title} at {job.company}!')
            return redirect('my_applications')
    else:
        form = JobApplicationForm()
    return render(request, 'alumni/job_apply.html', {'form': form, 'job': job})

@login_required
def job_create(request):
    # Only admin/staff can post jobs
    if not request.user.is_staff:
        messages.error(request, '⛔ Only administrators can post jobs.')
        return redirect('job_list')
    if request.method == 'POST':
        form = JobOpportunityForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.posted_by = request.user
            job.save()
            messages.success(request, '✅ Job posted successfully!')
            return redirect('job_list')
    else:
        form = JobOpportunityForm()
    return render(request, 'alumni/job_form.html', {'form': form, 'title': 'Post Job Opportunity'})

@login_required
def my_applications(request):
    applications = JobApplication.objects.filter(
        applicant=request.user).order_by('-applied_date')
    return render(request, 'alumni/my_applications.html', {'applications': applications})

@login_required
def withdraw_application(request, pk):
    application = get_object_or_404(JobApplication, pk=pk, applicant=request.user)
    if application.status not in ['offered', 'rejected']:
        application.status = 'withdrawn'
        application.save()
        messages.success(request, 'Application withdrawn successfully.')
    return redirect('my_applications')

# ── EVENTS ────────────────────────────────────────────────────────────────────

@login_required
def event_list(request):
    events = Event.objects.filter(date__gte=timezone.now()).order_by('date')
    return render(request, 'alumni/event_list.html', {'events': events})

@login_required
def event_create(request):
    # Only admin/staff can create events
    if not request.user.is_staff:
        messages.error(request, '⛔ Only administrators can create events.')
        return redirect('event_list')
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user
            event.save()
            messages.success(request, '✅ Event created successfully!')
            return redirect('event_list')
    else:
        form = EventForm()
    return render(request, 'alumni/event_form.html', {'form': form, 'title': 'Create Event'})

# ── AI ADVISOR ────────────────────────────────────────────────────────────────

@login_required
def ai_advisor(request):
    return render(request, 'alumni/ai_advisor.html')

@login_required
def ai_advisor_api(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    try:
        body = json.loads(request.body)
        user_message = body.get('message', '').strip()
        if not user_message:
            return JsonResponse({'error': 'No message provided'}, status=400)

        try:
            profile = Alumni.objects.get(user=request.user)
            context = f"The user has a {profile.degree} in {profile.major}, graduated in {profile.graduation_year}."
            if profile.current_job:
                context += f" Currently working as {profile.current_job}"
            if profile.company:
                context += f" at {profile.company}."
        except Alumni.DoesNotExist:
            context = "The user is an alumni seeking career guidance."

        system_prompt = f"""You are an expert career advisor for university alumni. {context}
Give practical, specific, actionable career advice. Be warm and encouraging.
Use short paragraphs. Always end with 2-3 concrete next steps the person can take this week."""

        payload = json.dumps({
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            "max_tokens": 1000,
            "temperature": 0.7
        }).encode('utf-8')

        req = urllib.request.Request(
            'https://api.groq.com/openai/v1/chat/completions',
            data=payload,
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {os.environ.get("GROQ_API_KEY", "")}',
                'User-Agent': 'Mozilla/5.0',
            },
            method='POST'
        )

        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode('utf-8'))
            reply = data['choices'][0]['message']['content']
            return JsonResponse({'reply': reply})

    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        return JsonResponse({'error': f'API error: {error_body}'}, status=500)
    except Exception as e:
        import traceback
        return JsonResponse({'error': str(e), 'trace': traceback.format_exc()}, status=500)