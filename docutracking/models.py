from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    """Base user model for both students and faculty"""
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('faculty', 'Faculty'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    phone = models.CharField(max_length=20, blank=True)
    official_email = models.EmailField(max_length=254, blank=True, help_text="Official email address for faculty users")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.username} ({self.role})"



class Student(models.Model):
    """Extended student profile information"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    student_id = models.CharField(max_length=20, unique=True)  # e.g., CS2024095
    department = models.CharField(max_length=100, default='Computer Science')
    semester = models.IntegerField(default=1)
    batch = models.CharField(max_length=20, blank=True)  # e.g., CS-A, CS-B
    enrollment_year = models.IntegerField(default=2024)
    assigned_faculty = models.ForeignKey('Faculty', on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_students')
    project_title = models.CharField(max_length=255, blank=True)
    address = models.TextField(blank=True)
    alternate_email = models.EmailField(blank=True)
    
    def __str__(self):
        return f"{self.student_id} - {self.user.get_full_name()}"


class Faculty(models.Model):
    """Extended faculty profile information"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='faculty_profile')
    faculty_id = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=100, default='Computer Science')
    designation = models.CharField(max_length=100, default='Professor')
    
    def __str__(self):
        return f"{self.faculty_id} - {self.user.get_full_name()}"


class Document(models.Model):
    """Document model for tracking uploaded files"""
    STATUS_CHOICES = (
        ('pending', 'Pending Review'),
        ('approved', 'Verified'),
        ('rejected', 'Action Required'),
    )
    
    CATEGORY_CHOICES = (
        ('project_report', 'Project Report / Abstract'),
        ('certificate', 'Internship / Course Certificate'),
        ('personal_id', 'Personal Identity Document'),
        ('other', 'Other Academic Record'),
    )
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='documents')
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='documents/%Y/%m/%d/')
    file_size = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    remarks = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_documents')
    
    def __str__(self):
        return f"{self.student.student_id} - {self.title} ({self.status})"
    
    @property
    def get_status_display_class(self):
        """Return CSS class based on status"""
        status_classes = {
            'pending': 'badge-pending',
            'approved': 'badge-approved',
            'rejected': 'badge-rejected',
        }
        return status_classes.get(self.status, 'badge-pending')


class BroadcastNotice(models.Model):
    """Model for faculty to broadcast notices to students"""
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='broadcasts')
    title = models.CharField(max_length=255)
    message = models.TextField()
    target_department = models.CharField(max_length=100, blank=True, help_text="Leave blank for all departments")
    target_batch = models.CharField(max_length=20, blank=True, help_text="Leave blank for all batches")
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.title} - {self.faculty.user.get_full_name()}"
    
    class Meta:
        ordering = ['-created_at']
