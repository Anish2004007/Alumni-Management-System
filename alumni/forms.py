from django import forms
from .models import Alumni, JobOpportunity, JobApplication, Event, Donation

class AlumniForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Alumni
        fields = ['first_name','last_name','email','student_id','phone','address','graduation_year','degree','major','current_job','company','linkedin','photo','bio']
        widgets = {
            'student_id': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'graduation_year': forms.Select(attrs={'class': 'form-select'}),
            'degree': forms.Select(attrs={'class': 'form-select'}),
            'major': forms.TextInput(attrs={'class': 'form-control'}),
            'current_job': forms.TextInput(attrs={'class': 'form-control'}),
            'company': forms.TextInput(attrs={'class': 'form-control'}),
            'linkedin': forms.URLInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email

class JobOpportunityForm(forms.ModelForm):
    class Meta:
        model = JobOpportunity
        fields = ['title','company','description','location','job_type','salary','requirements','contact_email','application_deadline']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Software Engineer'}),
            'company': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Google'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe the role...'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Mumbai, Remote'}),
            'job_type': forms.Select(attrs={'class': 'form-select'}),
            'salary': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. ₹8-12 LPA'}),
            'requirements': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'List key requirements...'}),
            'contact_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'application_deadline': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['cover_letter', 'resume_link']
        widgets = {
            'cover_letter': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 6,
                'placeholder': 'Write a compelling cover letter explaining why you are a great fit for this role...'
            }),
            'resume_link': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://drive.google.com/your-resume or LinkedIn URL'
            }),
        }

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title','description','date','location','registration_fee','max_participants']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'registration_fee': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'max_participants': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ['amount','purpose','is_recurring']
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'purpose': forms.TextInput(attrs={'class': 'form-control'}),
            'is_recurring': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class SearchForm(forms.Form):
    query = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Search by name, company, major...', 'class': 'form-control'}))
    graduation_year = forms.ChoiceField(choices=[('', 'Any Year')] + [(str(y), str(y)) for y in range(2000, 2031)], required=False, widget=forms.Select(attrs={'class': 'form-select'}))
    degree = forms.ChoiceField(choices=[('', 'Any Degree')] + Alumni.DEGREE_CHOICES, required=False, widget=forms.Select(attrs={'class': 'form-select'}))