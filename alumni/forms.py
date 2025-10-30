alumni/forms.py
from django import forms
from .models import Alumni, Event, Announcement
class AlumniForm(forms.ModelForm):
     class Meta:
            model = Alumni
            fields = ['name', 'email', 'graduation_year', 'profession', 'work_history', 'contact_number']
            widgets = {
                    'work_history': forms.Textarea(attrs={'rows': 3}),
            }
class EventForm(forms.ModelForm):
        class Meta:
            model = Event
            fields = ['title', 'description', 'date']
            widgets = {
                    'description': forms.Textarea(attrs={'rows': 3}),
                    'date': forms.DateInput(attrs={'type': 'date'}),
        }
class AnnouncementForm(forms.ModelForm):
        class Meta:
              model = Announcement
              fields = ['title', 'content']
              widgets = {
                        'content': forms.Textarea(attrs={'rows': 3}),
        }
