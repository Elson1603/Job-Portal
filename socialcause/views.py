from django.http import HttpResponse
from django.shortcuts import render
from django.urls import path

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.contrib.auth import logout
from django.forms import formset_factory

from .forms import SignUpForm, LoginForm, UserProfileForm
from .models import UserProfile

from django.urls import reverse
from .models import Resume, ResumeTemplate, Education, Experience, Skill, Project
from .forms import ResumeBasicInfoForm, EducationForm, ExperienceForm, SkillForm, ProjectForm
import json
from weasyprint import HTML
from django.template.loader import render_to_string
from django.shortcuts import render, redirect, get_object_or_404

def homepage(request):
    
    return render(request,"index.html")

def login_view(request):
    return render(request, 'login.html')

def profile_view(request):
    return render(request, 'profile.html')

def dashboard(request):
    return render(request, 'dashboard.html')

def base_resume(request):
    return render(request, 'base_resume.html')

def edit_resume_basic(request, resume_id):
    # Your logic to edit resume experience here
    return render(request, 'edit_basic.html', {'resume_id': resume_id})

def edit_resume_experience(request, resume_id):
    # Your logic to edit resume experience here
    return render(request, 'edit_experience.html', {'resume_id': resume_id})


def edit_resume_skills(request, resume_id):
    # Your logic to edit resume skills here
    return render(request, 'edit_skills.html', {'resume_id': resume_id})

def edit_resume_projects(request, resume_id):
    # Your logic to edit resume projects here
    return render(request, 'edit_projects.html', {'resume_id': resume_id})

def create_resume(request):
    return render(request, 'create_resume.html')

def choose_template(request):
    return render(request, 'choose_template.html')
def news1(request):
    return render(request, 'news1.html')

def news2(request):
    return render(request, 'news2.html')


def news3(request):
    return render(request, 'news3.html')


def jobapply(request):
    return render(request, 'jobapply.html')

def jobpost(request):
    return render(request, 'jobpost.html')

def builder(request):
    return render(request, 'builder.html')

def interview(request):
    return render(request, 'interview.html')

def info(request):
    return render(request, 'info.html')

def fullstack(request):
    return render(request, 'fullstack.html')

def frontend(request):
    return render(request, 'frontend.html')

def productmanager(request):
    return render(request, 'productmanager.html')

def ui(request):
    return render(request, 'ui.html')

def data(request):
    return render(request, 'data.html')

def backendeng(request):
    return render(request, 'backendeng.html')

def qa(request):
    return render(request, 'qa.html')

def cloud(request):
    return render(request, 'cloud.html')

def machine(request):
    return render(request, 'machine.html')

def cyber(request):
    return render(request, 'cyber.html')

def ai(request):
    return render(request, 'ai.html')

def network(request):
    return render(request, 'network.html')

def database(request):
    return render(request, 'database.html')

def blockchain(request):
    return render(request, 'blockchain.html')

def mnc(request):
    return render(request, 'mnc.html')

def internet(request):
    return render(request, 'internet.html')

def fortune(request):
    return render(request, 'fortune.html')

def product(request):
    return render(request, 'product.html')

def manufacture(request):
    return render(request, 'manufacture.html')

def dev(request):
    return render(request, 'dev.html')

def manager(request):
    return render(request, 'manager.html')

def mobile(request):
    return render(request, 'mobile.html')

def lead(request):
    return render(request, 'lead.html')

def services(request):
    return render(request, 'services.html')

def blog(request):
    return render(request, 'blog.html')

def dashboard(request):
    return render(request, 'dashboard.html')

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)
        
        if form.is_valid() and profile_form.is_valid():
            with transaction.atomic():
                user = form.save()
                profile = profile_form.save(commit=False)
                profile.user = user
                # Save other_skills from form
                profile.other_skills = profile_form.cleaned_data.get('other_skills', '')
                profile.save()
                
                # Save many-to-many relationships
                profile_form.save_m2m()
                
                # Log the user in
                user.backend = 'django.contrib.auth.backends.ModelBackend'  # Set backend explicitly
                login(request, user)
                messages.success(request, 'Account created successfully!')
                return redirect('profile')
    else:
        form = SignUpForm()
        profile_form = UserProfileForm()
    
    return render(request, 'signup.html', {
        'form': form,
        'profile_form': profile_form
    })

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.first_name}!')
                return redirect('index')
            else:
                messages.error(request, 'Invalid email or password.')
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'form': form})

@login_required
def profile_view(request):
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.other_skills = form.cleaned_data.get('other_skills', '')
            profile.save()
            form.save_m2m()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile)
    
    return render(request, 'profile.html', {'form': form})


def logout_view(request):
    # Get username before logout for message
    user_name = request.user.first_name if request.user.is_authenticated else ""
    
    # Log the user out (clears session)
    logout(request)
    
    # Add a success message
   
    
    # Redirect to login page
    return redirect('index')







@login_required
def resume_dashboard(request):
    resumes = Resume.objects.filter(user=request.user)
    return render(request, 'dashboard.html', {
        'resumes': resumes
    })

@login_required
def create_resume(request):
    templates = ResumeTemplate.objects.all()
    return render(request, 'choose_template.html', {
        'templates': templates
    })

@login_required
def edit_resume_basic(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    
    if request.method == 'POST':
        form = ResumeBasicInfoForm(request.POST, instance=resume)
        if form.is_valid():
            form.save()
            messages.success(request, "Basic information saved successfully!")
            return redirect('edit_resume_education', resume_id=resume.id)
    else:
        form = ResumeBasicInfoForm(instance=resume)
    
    return render(request, 'edit_basic.html', {
        'form': form,
        'resume': resume
    })

@login_required
def edit_resume_education(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    EducationFormSet = formset_factory(EducationForm, extra=1)
    
    if request.method == 'POST':
        formset = EducationFormSet(request.POST, prefix='education')
        if formset.is_valid():
            # Clear existing education entries
            Education.objects.filter(resume=resume).delete()
            
            # Save new education entries
            for form in formset:
                if form.cleaned_data and not form.empty_permitted:
                    education = form.save(commit=False)
                    education.resume = resume
                    education.save()
            
            messages.success(request, "Education information saved successfully!")
            return redirect('edit_resume_experience', resume_id=resume.id)
    else:
        # Pre-populate with existing education entries
        initial_data = [
            {
                'institution': edu.institution,
                'degree': edu.degree,
                'field_of_study': edu.field_of_study,
                'start_date': edu.start_date,
                'end_date': edu.end_date,
                'current': edu.current,
                'description': edu.description
            }
            for edu in resume.education.all()
        ]
        
        if not initial_data:
            formset = EducationFormSet(prefix='education')
        else:
            formset = EducationFormSet(initial=initial_data, prefix='education')
    
    return render(request, 'resume/edit_education.html', {
        'formset': formset,
        'resume': resume
    })

# Similar views for experience, skills, and projects...

@login_required
def preview_resume(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    
    return render(request, 'resume/preview.html', {
        'resume': resume
    })

@login_required
def download_resume_pdf(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    
    # Render HTML content
    html_string = render_to_string('resume/pdf_template.html', {'resume': resume})
    
    # Create PDF
    html = HTML(string=html_string, base_url=request.build_absolute_uri('/'))
    pdf = html.write_pdf()
    
    # Create HTTP response with PDF
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{resume.title}.pdf"'
    
    return response


# Example of what your view might need to look like
def choose_template(request):
    templates = ResumeTemplate.objects.all()  # Or your query logic
    return render(request, 'your_template_name.html', {'templates': templates})