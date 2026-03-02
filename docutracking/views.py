from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.utils import timezone
from django.views.decorators.clickjacking import xframe_options_exempt
from django.db import models
from .models import User, Student, Faculty, Document, BroadcastNotice



def index_view(request):
    """Landing page view"""
    return render(request, 'index.html')


def login_view(request):
    """Login page view with role-based authentication"""
    if request.user.is_authenticated:
        # Redirect based on role
        if request.user.role == 'student':
            return redirect('student_dashboard')
        else:
            return redirect('faculty_dashboard')
    
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        password = request.POST.get('password')
        
        # Authenticate user
        user = authenticate(request, username=user_id, password=password)
        
        if user is not None:
            login(request, user)
            
            # Redirect based on role
            if user.role == 'student':
                return redirect('student_dashboard')
            elif user.role == 'faculty':
                return redirect('faculty_dashboard')
            else:
                return redirect('index')
        else:
            messages.error(request, 'Invalid credentials. Please try again.')
    
    return render(request, 'login.html')


def register_view(request):
    """Registration page view"""
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role', 'student')
        
        # Check if user already exists
        if User.objects.filter(username=user_id).exists():
            messages.error(request, 'User ID already exists.')
            return render(request, 'register.html')
        
        # Create user
        user = User.objects.create_user(
            username=user_id,
            email=email,
            password=password,
            role=role
        )
        
        # Create Student or Faculty profile
        if role == 'student':
            Student.objects.create(
                user=user,
                student_id=user_id,
                department='Computer Science',
                semester=1
            )
        
        messages.success(request, 'Registration successful! Please login.')
        return redirect('login')
    
    return render(request, 'register.html')


def logout_view(request):
    """Logout user and redirect to index"""
    logout(request)
    return redirect('index')


@login_required
def student_dashboard_view(request):
    """Student dashboard view with dynamic data"""
    # Check if user is a student
    if request.user.role != 'student':
        return HttpResponseForbidden("Access denied.")
    
    try:
        student = request.user.student_profile
    except Student.DoesNotExist:
        messages.error(request, 'Student profile not found. Please contact administrator.')
        logout(request)
        return redirect('login')
    
    # Get student's documents
    documents = Document.objects.filter(student=student).order_by('-submitted_at')
    
    # Calculate stats
    total_docs = documents.count()
    pending_docs = documents.filter(status='pending').count()
    approved_docs = documents.filter(status='approved').count()
    rejected_docs = documents.filter(status='rejected').count()
    
    context = {
        'student': student,
        'documents': documents,
        'total_docs': total_docs,
        'pending_docs': pending_docs,
        'approved_docs': approved_docs,
        'rejected_docs': rejected_docs,
    }
    
    return render(request, 'student_dashboard.html', context)


@login_required
def faculty_dashboard_view(request):
    """Faculty dashboard view with dynamic data"""
    # Check if user is a faculty
    if request.user.role != 'faculty':
        return HttpResponseForbidden("Access denied.")
    
    try:
        faculty = request.user.faculty_profile
    except Faculty.DoesNotExist:
        # Auto-create faculty profile if it doesn't exist
        faculty = Faculty.objects.create(
            user=request.user,
            faculty_id=request.user.username,
            department='Computer Science',
            designation='Professor'
        )
        messages.info(request, 'Faculty profile was auto-created for you.')
    
    # Get all pending documents from all students
    pending_documents = Document.objects.filter(status='pending').order_by('-submitted_at')
    
    # Get today's verified documents
    today = timezone.now().date()
    verified_today = Document.objects.filter(
        status='approved', 
        reviewed_at__date=today
    ).count()
    
    # Get total students
    total_students = Student.objects.count()
    
    # Get flagged issues (rejected documents)
    flagged_issues = Document.objects.filter(status='rejected').count()
    
    # Get all students for batch info
    students = Student.objects.all()
    
    context = {
        'faculty': faculty,
        'pending_documents': pending_documents,
        'verified_today': verified_today,
        'total_students': total_students,
        'flagged_issues': flagged_issues,
        'students': students,
    }
    
    return render(request, 'faculty_dashboard.html', context)


@login_required
def student_profile_view(request):
    """Student profile view with dynamic data"""
    # Check if user is a student
    if request.user.role != 'student':
        return HttpResponseForbidden("Access denied.")
    
    try:
        student = request.user.student_profile
    except Student.DoesNotExist:
        messages.error(request, 'Student profile not found. Please contact administrator.')
        logout(request)
        return redirect('login')
    
    if request.method == 'POST':
        # Update phone in User model
        request.user.phone = request.POST.get('phone', request.user.phone)
        request.user.save()
        
        # Update student profile
        student.alternate_email = request.POST.get('alternate_email', student.alternate_email)
        student.address = request.POST.get('address', student.address)
        student.semester = request.POST.get('semester', student.semester)
        student.project_title = request.POST.get('project_title', student.project_title)
        
        student.save()
        messages.success(request, 'Profile updated successfully!')
    
    context = {
        'student': student,
        'user': request.user,
    }
    
    return render(request, 'student_profile.html', context)


@login_required
def document_upload_view(request):
    """Document upload view with file handling"""
    # Check if user is a student
    if request.user.role != 'student':
        return HttpResponseForbidden("Access denied.")
    
    try:
        student = request.user.student_profile
    except Student.DoesNotExist:
        messages.error(request, 'Student profile not found. Please contact administrator.')
        logout(request)
        return redirect('login')
    
    if request.method == 'POST':
        title = request.POST.get('title')
        category = request.POST.get('category')
        description = request.POST.get('description')
        uploaded_file = request.FILES.get('file_upload')
        
        if uploaded_file:
            # Create document record
            document = Document.objects.create(
                student=student,
                title=title or uploaded_file.name,
                category=category,
                description=description,
                file=uploaded_file,
                file_size=uploaded_file.size,
                status='pending'
            )
            
            messages.success(request, 'Document uploaded successfully!')
            return redirect('student_dashboard')
        else:
            messages.error(request, 'Please select a file to upload.')
    
    context = {
        'student': student,
    }
    
    return render(request, 'document_upload.html', context)


@login_required
@xframe_options_exempt
def verification_detail_view(request, doc_id=None):
    """Verification detail view with approve/reject functionality"""

    # Check if user is a faculty
    if request.user.role != 'faculty':
        return HttpResponseForbidden("Access denied.")
    
    try:
        faculty = request.user.faculty_profile
    except Faculty.DoesNotExist:
        # Auto-create faculty profile if it doesn't exist
        faculty = Faculty.objects.create(
            user=request.user,
            faculty_id=request.user.username,
            department='Computer Science',
            designation='Professor'
        )
        messages.info(request, 'Faculty profile was auto-created for you.')
    
    if not doc_id:
        messages.error(request, 'Document ID required.')
        return redirect('faculty_dashboard')
    
    try:
        document = Document.objects.select_related('student', 'student__user').get(id=doc_id)
    except Document.DoesNotExist:
        messages.error(request, 'Document not found.')
        return redirect('faculty_dashboard')
    
    # Handle approval/rejection
    if request.method == 'POST':
        action = request.POST.get('action')
        remarks = request.POST.get('remarks', '')
        
        if action == 'approve':
            document.status = 'approved'
            document.remarks = remarks
        elif action == 'reject':
            document.status = 'rejected'
            document.remarks = remarks
        
        document.reviewed_by = faculty
        document.reviewed_at = timezone.now()
        document.save()
        
        if action == 'approve':
            messages.success(request, 'Document verified successfully!')
        else:
            messages.warning(request, 'Document returned for revision.')
        
        return redirect('faculty_dashboard')
    
    context = {
        'document': document,
        'faculty': faculty,
    }
    
    return render(request, 'verification_detail.html', context)


@login_required
def faculty_students_view(request):
    """Faculty student database view with search and filter"""
    # Check if user is a faculty
    if request.user.role != 'faculty':
        return HttpResponseForbidden("Access denied.")
    
    try:
        faculty = request.user.faculty_profile
    except Faculty.DoesNotExist:
        messages.error(request, 'Faculty profile not found.')
        return redirect('faculty_dashboard')
    
    # Get search and filter parameters
    search_query = request.GET.get('search', '')
    batch_filter = request.GET.get('batch', '')
    department_filter = request.GET.get('department', '')
    
    # Base queryset
    students = Student.objects.select_related('user').all()
    
    # Apply filters
    if search_query:
        students = students.filter(
            models.Q(student_id__icontains=search_query) |
            models.Q(user__first_name__icontains=search_query) |
            models.Q(user__last_name__icontains=search_query) |
            models.Q(project_title__icontains=search_query)
        )
    
    if batch_filter:
        students = students.filter(batch=batch_filter)
    
    if department_filter:
        students = students.filter(department=department_filter)
    
    # Get unique batches and departments for filter dropdowns
    batches = Student.objects.values_list('batch', flat=True).distinct()
    departments = Student.objects.values_list('department', flat=True).distinct()
    
    # Get document stats for each student
    student_stats = {}
    for student in students:
        docs = student.documents.all()
        student_stats[student.id] = {
            'total': docs.count(),
            'pending': docs.filter(status='pending').count(),
            'approved': docs.filter(status='approved').count(),
            'rejected': docs.filter(status='rejected').count(),
        }
    
    context = {
        'faculty': faculty,
        'students': students,
        'batches': batches,
        'departments': departments,
        'student_stats': student_stats,
        'search_query': search_query,
        'batch_filter': batch_filter,
        'department_filter': department_filter,
    }
    
    return render(request, 'faculty_students.html', context)


@login_required
def faculty_batch_approvals_view(request):
    """Faculty batch approvals view with bulk actions"""
    # Check if user is a faculty
    if request.user.role != 'faculty':
        return HttpResponseForbidden("Access denied.")
    
    try:
        faculty = request.user.faculty_profile
    except Faculty.DoesNotExist:
        messages.error(request, 'Faculty profile not found.')
        return redirect('faculty_dashboard')
    
    # Get filter parameters
    batch_filter = request.GET.get('batch', '')
    category_filter = request.GET.get('category', '')
    status_filter = request.GET.get('status', 'pending')
    
    # Base queryset
    documents = Document.objects.select_related('student', 'student__user').order_by('-submitted_at')
    
    # Apply filters
    if batch_filter:
        documents = documents.filter(student__batch=batch_filter)
    
    if category_filter:
        documents = documents.filter(category=category_filter)
    
    if status_filter:
        documents = documents.filter(status=status_filter)
    
    # Get unique batches for filter dropdown
    batches = Student.objects.values_list('batch', flat=True).distinct()
    
    # Handle bulk actions
    if request.method == 'POST':
        selected_docs = request.POST.getlist('selected_docs')
        action = request.POST.get('action')
        bulk_remarks = request.POST.get('remarks', '')
        
        if selected_docs and action:
            if action in ['approve', 'reject']:
                updated_count = Document.objects.filter(id__in=selected_docs).update(
                    status='approved' if action == 'approve' else 'rejected',
                    remarks=bulk_remarks,
                    reviewed_by=faculty,
                    reviewed_at=timezone.now()
                )
                
                if action == 'approve':
                    messages.success(request, f'{updated_count} documents approved successfully!')
                else:
                    messages.warning(request, f'{updated_count} documents marked for revision.')
                
                return redirect('faculty_batch_approvals')
            else:
                messages.error(request, 'Invalid action.')
    
    # Group documents by batch for display
    documents_by_batch = {}
    for doc in documents:
        batch = doc.student.batch or 'Unknown'
        if batch not in documents_by_batch:
            documents_by_batch[batch] = []
        documents_by_batch[batch].append(doc)
    
    context = {
        'faculty': faculty,
        'documents': documents,
        'documents_by_batch': documents_by_batch,
        'batches': batches,
        'batch_filter': batch_filter,
        'category_filter': category_filter,
        'status_filter': status_filter,
    }
    
    return render(request, 'faculty_batch_approvals.html', context)


@login_required
def faculty_settings_view(request):
    """Faculty settings view"""
    # Check if user is a faculty
    if request.user.role != 'faculty':
        return HttpResponseForbidden("Access denied.")
    
    try:
        faculty = request.user.faculty_profile
    except Faculty.DoesNotExist:
        # Auto-create faculty profile if it doesn't exist
        faculty = Faculty.objects.create(
            user=request.user,
            faculty_id=request.user.username,
            department='Computer Science',
            designation='Professor'
        )
        messages.info(request, 'Faculty profile was auto-created for you.')
    
    if request.method == 'POST':
        # Update user profile
        request.user.first_name = request.POST.get('first_name', request.user.first_name)
        request.user.last_name = request.POST.get('last_name', request.user.last_name)
        request.user.email = request.POST.get('email', request.user.email)
        request.user.phone = request.POST.get('phone', request.user.phone)
        request.user.save()
        
        # Update faculty profile
        faculty.designation = request.POST.get('designation', faculty.designation)
        faculty.department = request.POST.get('department', faculty.department)
        faculty.save()
        
        messages.success(request, 'Settings updated successfully!')
    
    context = {
        'faculty': faculty,
        'user': request.user,
    }
    
    return render(request, 'faculty_settings.html', context)


@login_required
def broadcast_notice_view(request):
    """Broadcast notice view for faculty to send notices to students"""
    # Check if user is a faculty
    if request.user.role != 'faculty':
        return HttpResponseForbidden("Access denied.")
    
    try:
        faculty = request.user.faculty_profile
    except Faculty.DoesNotExist:
        messages.error(request, 'Faculty profile not found.')
        return redirect('faculty_dashboard')
    
    if request.method == 'POST':
        title = request.POST.get('title')
        message = request.POST.get('message')
        target_department = request.POST.get('target_department', '')
        target_batch = request.POST.get('target_batch', '')
        
        if title and message:
            broadcast = BroadcastNotice.objects.create(
                faculty=faculty,
                title=title,
                message=message,
                target_department=target_department,
                target_batch=target_batch
            )
            messages.success(request, f'Notice "{title}" broadcasted successfully!')
            return redirect('faculty_dashboard')
        else:
            messages.error(request, 'Please fill in all required fields.')
    
    # Get previous broadcasts
    broadcasts = BroadcastNotice.objects.filter(faculty=faculty)[:10]
    
    # Get departments and batches for targeting
    departments = Student.objects.values_list('department', flat=True).distinct()
    batches = Student.objects.values_list('batch', flat=True).distinct()
    
    context = {
        'faculty': faculty,
        'broadcasts': broadcasts,
        'departments': departments,
        'batches': batches,
    }
    
    return render(request, 'faculty_broadcast.html', context)
