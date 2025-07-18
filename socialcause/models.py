# socialcause/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

# Custom User model
class User(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        app_label = 'socialcause'

    def __str__(self):
        return self.email

# Job Type model
class JobType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# General Skill model
class Skill(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# UserProfile model
class UserProfile(models.Model):
    EXPERIENCE_CHOICES = [
        ('0-1', 'Less than 1 year'),
        ('1-3', '1-3 years'),
        ('3-5', '3-5 years'),
        ('5+', 'More than 5 years'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    skills = models.ManyToManyField(Skill, blank=True)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    preferred_job_types = models.ManyToManyField(JobType, blank=True)
    work_experience = models.CharField(max_length=3, choices=EXPERIENCE_CHOICES, blank=True, null=True)
    portfolio_link = models.URLField(blank=True, null=True)
    other_skills = models.CharField(max_length=255, blank=True, null=True)  # New field for custom skills

    def __str__(self):
        return f"{self.user.email}'s Profile"

# ResumeTemplate model
class ResumeTemplate(models.Model):
    name = models.CharField(max_length=100)
    preview_image = models.ImageField(upload_to='resume_templates/', null=True, blank=True)
    html_structure = models.TextField()  # HTML template for this resume design

    def __str__(self):
        return self.name

# Resume model
class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resumes')
    title = models.CharField(max_length=100)
    template = models.ForeignKey(ResumeTemplate, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Basic Info
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField(blank=True, null=True)
    summary = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.title} - {self.user.username}"

# Education model
class Education(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='education')
    institution = models.CharField(max_length=100)
    degree = models.CharField(max_length=100)
    field_of_study = models.CharField(max_length=100, blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    current = models.BooleanField(default=False)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.degree} at {self.institution}"

# Experience model
class Experience(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='experiences')
    company = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    location = models.CharField(max_length=100, blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    current = models.BooleanField(default=False)
    description = models.TextField()
    
    def __str__(self):
        return f"{self.position} at {self.company}"

# ResumeSkill model (linked to a resume)
class ResumeSkill(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='skills')  # Link to the Resume model
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='resume_skills')  # Link to the Skill model
    level = models.IntegerField(choices=[(1, 'Beginner'), (2, 'Intermediate'), (3, 'Advanced'), (4, 'Expert')], default=2)
    
    def __str__(self):
        return self.name

# Project model
class Project(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=100)
    description = models.TextField()
    url = models.URLField(blank=True, null=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return self.title
