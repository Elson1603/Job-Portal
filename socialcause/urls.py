
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from socialcause import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('index.html', views.homepage, name='index'),
    path('signup/', views.signup_view, name='signup'),
    path('login.html', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile.html', views.profile_view, name='profile'),
    path('', RedirectView.as_view(pattern_name='login', permanent=False)),
    path('dashboard/', views.dashboard, name='dashboard'), 
    path('create_resume.html', views.create_resume, name='create_resume'),
    path('choose_template.html', views.choose_template, name='choose_template'),
    path('edit_basic.html', views.edit_resume_basic, name='edit_resume_basic'),
    path('<int:resume_id>/edit/education/', views.edit_resume_education, name='edit_resume_education'),
    path('<int:resume_id>/edit/experience/', views.edit_resume_experience, name='edit_resume_experience'),
    path('<int:resume_id>/edit/skills/', views.edit_resume_skills, name='edit_resume_skills'),
    path('<int:resume_id>/edit/projects/', views.edit_resume_projects, name='edit_resume_projects'),
    path('<int:resume_id>/preview/', views.preview_resume, name='preview_resume'),
    path('<int:resume_id>/download-pdf/', views.download_resume_pdf, name='download_resume_pdf'),
    path('news1.html', views.news1, name='news1'),
    path('news2.html', views.news2, name='news2'),
    path('news3.html', views.news3, name='news3'),
    path('jobapply.html', views.jobapply, name='jobapply'),
    path('jobpost.html', views.jobpost, name='jobpost'),
    path('builder.html', views.builder, name='builder'),
    path('interview.html', views.interview, name='interview'),
    path('info.html', views.info, name='info'),
    path('fullstack.html', views.fullstack, name='fullstack'),
    path('frontend.html', views.frontend, name='frontend'),
    path('dev.html', views.dev, name='dev'),
    path('manager.html', views.manager, name='manager'),
    path('mobile.html', views.mobile, name='mobile'),
    path('lead.html', views.lead, name='lead'),
    path('productmanager.html', views.productmanager, name='productmanager'),
    path('ui.html', views.ui, name='ui'),
    path('data.html', views.data, name='data'),
    path('backendeng.html', views.backendeng, name='backendeng'),
    path('qa.html', views.qa, name= 'qa'),
    path('cloud.html', views.cloud, name= 'cloud'),
    path('machine.html', views.machine, name= 'machine'),
    path('cyber.html', views.cyber, name= 'cyber'),
     path('ai.html', views.ai, name= 'ai'),
     path('network.html', views.network, name= 'network'),
    path('database.html', views.database, name= 'database'),
    path('blockchain.html', views.blockchain, name= 'blockchain'),
    path('mnc.html', views.mnc, name= 'mnc'),
    path('internet.html', views.internet, name= 'internet'),
    path('fortune.html', views.fortune, name= 'fortune'),
    path('product.html', views.product, name= 'procduct'),
    path('manufacture.html', views.manufacture, name= 'manufacture'),
    path('services.html', views.services, name= 'services'),
    path('blog.html', views.blog, name= 'blog'),
    path('auth/', include('social_django.urls', namespace='social')),
]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
