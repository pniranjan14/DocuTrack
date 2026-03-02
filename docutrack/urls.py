"""
URL configuration for docutrack project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import os
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.http import FileResponse, Http404
from django.views.decorators.clickjacking import xframe_options_exempt
from docutracking import views


@xframe_options_exempt
def serve_pdf(request, path):
    """Serve PDF files with X-Frame-Options exempt to allow iframe embedding"""
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path) and file_path.endswith('.pdf'):
        return FileResponse(open(file_path, 'rb'), content_type='application/pdf')
    raise Http404("PDF not found")


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index_view, name='index'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('student/dashboard/', views.student_dashboard_view, name='student_dashboard'),
    path('faculty/dashboard/', views.faculty_dashboard_view, name='faculty_dashboard'),
    path('student/profile/', views.student_profile_view, name='student_profile'),
    path('document/upload/', views.document_upload_view, name='document_upload'),
    path('verification/<int:doc_id>/', views.verification_detail_view, name='verification_detail'),
    path('faculty/students/', views.faculty_students_view, name='faculty_students'),
    path('faculty/batch-approvals/', views.faculty_batch_approvals_view, name='faculty_batch_approvals'),
    path('faculty/settings/', views.faculty_settings_view, name='faculty_settings'),
    path('faculty/broadcast/', views.broadcast_notice_view, name='faculty_broadcast'),
    path('media/<path:path>', serve_pdf, name='serve_pdf'),
]

# Serve media files during development (only for non-PDF files)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
