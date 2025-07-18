# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.validators import RegexValidator
from .models import User, UserProfile, JobType, Skill, Resume, Education, Experience, Project, ResumeSkill

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    phone_number = forms.CharField(
        required=True, 
        validators=[ 
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
            )
        ]
    )
    location = forms.CharField(required=True)
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'phone_number', 'location', 'password1', 'password2')

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Email')
    
    class Meta:
        model = User
        fields = ('username', 'password')

class UserProfileForm(forms.ModelForm):
    skills = forms.ModelMultipleChoiceField(
        queryset=Skill.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    preferred_job_types = forms.ModelMultipleChoiceField(
        queryset=JobType.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    other_skills = forms.CharField(
        required=False,
        label='Other skills (comma separated)',
        widget=forms.TextInput(attrs={'placeholder': 'Enter other skills'})
    )
    
    class Meta:
        model = UserProfile
        fields = ('skills', 'other_skills', 'resume', 'profile_picture', 'preferred_job_types', 'work_experience', 'portfolio_link')

class ResumeBasicInfoForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['title', 'template', 'full_name', 'email', 'phone', 'address', 'summary']
        widgets = {
            'summary': forms.Textarea(attrs={'rows': 4}),
            'address': forms.Textarea(attrs={'rows': 2}),
        }

class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ['institution', 'degree', 'field_of_study', 'start_date', 'end_date', 'current', 'description']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = ['company', 'position', 'location', 'start_date', 'end_date', 'current', 'description']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['name']  # Removed 'level' as it's not in the Skill model

class ResumeSkillForm(forms.ModelForm):
    # Reference the `Skill` model to get the name
    skill_name = forms.CharField(
        required=False,
        label='Skill Name',
        widget=forms.TextInput(attrs={'readonly': 'readonly'})
    )

    class Meta:
        model = ResumeSkill
        fields = ['skill', 'level']  # Assuming 'skill' is a foreign key in ResumeSkill

    def __init__(self, *args, **kwargs):
        super(ResumeSkillForm, self).__init__(*args, **kwargs)
        # Automatically fill the `skill_name` field with the name of the associated skill
        if 'skill' in self.initial:
            skill = self.initial['skill']
            self.fields['skill_name'].initial = skill.name if skill else ''

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'url', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }
