from django import forms
from .models import Alumni, Event, Announcement

class AlumniForm(forms.ModelForm):
    class Meta:
        model = Alumni
        fields = ['name', 'email', 'graduation_year', 'profession', 'work_history', 'contact_number']

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'date']

class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'content']