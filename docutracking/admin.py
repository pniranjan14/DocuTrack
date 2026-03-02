from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django import forms
from docutracking.models import User, Student, Faculty, Document


class FacultyUserCreationForm(forms.ModelForm):
    """Custom form for creating faculty users through admin"""
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput,
        help_text="Enter a strong password for the faculty user"
    )
    password2 = forms.CharField(
        label='Password confirmation',
        widget=forms.PasswordInput,
        help_text="Enter the same password as above, for verification."
    )
    role = forms.ChoiceField(
        choices=User.ROLE_CHOICES,
        initial='faculty',
        help_text="Select user role"
    )
    designation = forms.CharField(max_length=100, initial='Professor', help_text="Faculty designation (e.g., Professor, Assistant Professor, Associate Professor)")
    department = forms.CharField(max_length=100, initial='Computer Science', help_text="Department name")
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'official_email', 'role', 'designation', 'department')

    
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.role = 'faculty'
        user.email = self.cleaned_data['official_email']
        
        if commit:
            user.save()
            # Create Faculty profile
            Faculty.objects.create(
                user=user,
                faculty_id=user.username,
                designation=self.cleaned_data['designation'],
                department=self.cleaned_data['department']
            )
        return user


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'official_email', 'first_name', 'last_name', 'role', 'is_staff', 'is_superuser')
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('role', 'phone', 'official_email')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'first_name', 'last_name', 'official_email', 'role', 'designation', 'department'),
        }),
    )
    
    def get_form(self, request, obj=None, **kwargs):
        """Use custom form when creating new users"""
        if obj is None:  # Creating new user
            return FacultyUserCreationForm
        return super().get_form(request, obj, **kwargs)
    
    def save_model(self, request, obj, form, change):
        """Override save to handle faculty profile creation"""
        if not change:  # Creating new user
            # Set email from official_email if provided
            if form.cleaned_data.get('official_email'):
                obj.email = form.cleaned_data['official_email']
            obj.role = form.cleaned_data.get('role', 'student')
        super().save_model(request, obj, form, change)
        
        # Create faculty profile if role is faculty and profile doesn't exist
        if obj.role == 'faculty' and not hasattr(obj, 'faculty_profile'):
            Faculty.objects.create(
                user=obj,
                faculty_id=obj.username,
                designation=form.cleaned_data.get('designation', 'Professor'),
                department=form.cleaned_data.get('department', 'Computer Science')
            )



@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'user', 'department', 'semester', 'batch', 'enrollment_year', 'assigned_faculty')
    list_filter = ('department', 'semester', 'batch', 'enrollment_year')
    search_fields = ('student_id', 'user__first_name', 'user__last_name', 'user__email')


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ('faculty_id', 'user', 'department', 'designation')
    list_filter = ('department', 'designation')
    search_fields = ('faculty_id', 'user__first_name', 'user__last_name', 'user__email')


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'student', 'category', 'status', 'submitted_at', 'reviewed_at')
    list_filter = ('status', 'category', 'submitted_at')
    search_fields = ('title', 'student__student_id', 'student__user__first_name')
