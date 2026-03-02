"""
Script to create sample data for DocuTrack application
Run with: python manage.py shell < create_sample_data.py
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'docutrack.settings')
django.setup()

from docutracking.models import User, Student, Faculty, Document
from django.utils import timezone
from datetime import timedelta

# Create Faculty User
faculty_user = User.objects.create_user(
    username='preynolds',
    email='prof.reynolds@college.edu',
    password='faculty123',
    first_name='Patricia',
    last_name='Reynolds',
    role='faculty',
    phone='+91 98765 43210'
)

# Create Faculty Profile
faculty = Faculty.objects.create(
    user=faculty_user,
    faculty_id='FAC001',
    department='Computer Science',
    designation='Professor & HOD'
)

# Create Student Users
students_data = [
    {
        'username': 'amorgan',
        'email': 'alex.morgan@college.edu',
        'password': 'student123',
        'first_name': 'Alex',
        'last_name': 'Morgan',
        'student_id': 'CS2024095',
        'department': 'Computer Science',
        'semester': 8,
        'batch': 'CS-A',
        'enrollment_year': 2024,
        'project_title': 'AI-Based Traffic Management System',
        'assigned_faculty': faculty,
        'phone': '+91 88452 99100',
        'address': '12/A, Tech Park View, Bangalore, India',
        'alternate_email': 'alex.morgan.personal@gmail.com'
    },
    {
        'username': 'sjenkins',
        'email': 'sarah.jenkins@college.edu',
        'password': 'student123',
        'first_name': 'Sarah',
        'last_name': 'Jenkins',
        'student_id': 'CS2026042',
        'department': 'Computer Science',
        'semester': 8,
        'batch': 'CS-A',
        'enrollment_year': 2026,
        'project_title': 'Smart Attendance System using Face Recognition',
        'assigned_faculty': faculty,
        'phone': '+91 98765 12345',
        'address': '45, Green Valley Apartments, Chennai, India',
        'alternate_email': ''
    },
    {
        'username': 'mchen',
        'email': 'marcus.chen@college.edu',
        'password': 'student123',
        'first_name': 'Marcus',
        'last_name': 'Chen',
        'student_id': 'CS2026088',
        'department': 'Computer Science',
        'semester': 8,
        'batch': 'CS-B',
        'enrollment_year': 2026,
        'project_title': 'E-Commerce Analytics Dashboard',
        'assigned_faculty': faculty,
        'phone': '+91 99887 76655',
        'address': '78, Ocean View, Mumbai, India',
        'alternate_email': ''
    },
    {
        'username': 'akhan',
        'email': 'aisha.khan@college.edu',
        'password': 'student123',
        'first_name': 'Aisha',
        'last_name': 'Khan',
        'student_id': 'CS2026012',
        'department': 'Computer Science',
        'semester': 8,
        'batch': 'CS-A',
        'enrollment_year': 2026,
        'project_title': 'Healthcare Monitoring IoT System',
        'assigned_faculty': faculty,
        'phone': '+91 91234 56789',
        'address': '101, Royal Residency, Delhi, India',
        'alternate_email': ''
    },
]

students = []
for data in students_data:
    user = User.objects.create_user(
        username=data['username'],
        email=data['email'],
        password=data['password'],
        first_name=data['first_name'],
        last_name=data['last_name'],
        role='student',
        phone=data['phone']
    )
    student = Student.objects.create(
        user=user,
        student_id=data['student_id'],
        department=data['department'],
        semester=data['semester'],
        batch=data['batch'],
        enrollment_year=data['enrollment_year'],
        project_title=data['project_title'],
        assigned_faculty=data['assigned_faculty'],
        address=data['address'],
        alternate_email=data['alternate_email']
    )
    students.append(student)

print("Created users and students successfully!")

# Create sample documents
documents_data = [
    # Alex Morgan's documents
    {
        'student': students[0],
        'title': 'Final_Project_Report_v2.pdf',
        'category': 'project_report',
        'description': 'Updated final project report with all sections completed',
        'status': 'pending',
        'remarks': ''
    },
    {
        'student': students[0],
        'title': 'Internship_Certificate.jpg',
        'category': 'certificate',
        'description': 'Certificate from Tech Solutions Pvt Ltd',
        'status': 'approved',
        'remarks': 'Validated by Prof. Smith',
        'reviewed_by': faculty
    },
    {
        'student': students[0],
        'title': 'Abstract_Draft.docx',
        'category': 'project_report',
        'description': 'Initial abstract draft',
        'status': 'rejected',
        'remarks': 'Format incorrect. Re-upload.'
    },
    # Sarah Jenkins' documents
    {
        'student': students[1],
        'title': 'Final_Project_Abstract.pdf',
        'category': 'project_report',
        'description': 'Revised abstract including traffic algorithm methodology',
        'status': 'pending',
        'remarks': ''
    },
    # Marcus Chen's documents
    {
        'student': students[2],
        'title': 'Internship_Certificate.pdf',
        'category': 'certificate',
        'description': 'Internship completion certificate from Amazon',
        'status': 'pending',
        'remarks': ''
    },
    # Aisha Khan's documents
    {
        'student': students[3],
        'title': 'Project_Phase1_Report.pdf',
        'category': 'project_report',
        'description': 'Phase 1 documentation and methodology',
        'status': 'approved',
        'remarks': 'Approved - Good work on literature survey',
        'reviewed_by': faculty
    },
]

for doc_data in documents_data:
    # Set reviewed_at for non-pending documents
    reviewed_at = None
    if doc_data['status'] != 'pending':
        reviewed_at = timezone.now() - timedelta(days=2)
    
    Document.objects.create(
        student=doc_data['student'],
        title=doc_data['title'],
        category=doc_data['category'],
        description=doc_data['description'],
        file=f"documents/sample/{doc_data['title']}",
        file_size=2400000,
        status=doc_data['status'],
        remarks=doc_data.get('remarks', ''),
        reviewed_by=doc_data.get('reviewed_by'),
        reviewed_at=reviewed_at
    )

print(f"Created {len(documents_data)} sample documents!")

# Print login credentials
print("\n=== Login Credentials ===")
print("Student: amorgan / student123")
print("Faculty: preynolds / faculty123")
