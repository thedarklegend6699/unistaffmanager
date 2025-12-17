from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

# -----------------------------
# Custom User Manager
# -----------------------------
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


# -----------------------------
# Department
# -----------------------------
class Department(models.Model):
    department_type = models.CharField(max_length=100)
    department_name = models.CharField(max_length=150)

    def __str__(self):
        return self.department_name


# -----------------------------
# Designation
# -----------------------------
class Designation(models.Model):
    designation_name = models.CharField(max_length=150)
    scale = models.CharField(max_length=50)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.designation_name


# -----------------------------
# Employee
# -----------------------------
class Employee(models.Model):
    employee_name = models.CharField(max_length=150)
    father_name = models.CharField(max_length=150)
    gender = models.CharField(max_length=20)
    designation = models.ForeignKey(Designation, on_delete=models.PROTECT, related_name='employees')
    department = models.ForeignKey(Department, on_delete=models.PROTECT, related_name='employees')
    domicile = models.CharField(max_length=100)
    cnic = models.CharField(max_length=20, unique=True)
    date_of_birth = models.DateField()
    date_of_joining = models.DateField()
    date_of_leaving = models.DateField(null=True, blank=True)
    retirement_date = models.DateField(null=True, blank=True)
    qualification = models.TextField()
    research_paper = models.TextField(blank=True)
    experience = models.IntegerField()
    leave_balance = models.IntegerField(default=0)

    def __str__(self):
        return self.employee_name


# -----------------------------
# User (1-to-1 with Employee)
# -----------------------------
class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name='user')
    management_role = models.CharField(max_length=150)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email


# -----------------------------
# Employee Management (Employee manages Employee)
# -----------------------------
class EmployeeManagement(models.Model):
    manager = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='managed_employees')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='managed_by')
    reason = models.TextField()
    managed_at = models.DateTimeField(auto_now_add=True)


# -----------------------------
# Employee Job History
# -----------------------------
class EmployeeJobHistory(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='job_history')
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)


# -----------------------------
# Attendance
# -----------------------------
class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='attendance_records')
    attendance_date = models.DateField()
    attendance_time = models.TimeField()
    direction = models.CharField(max_length=20)  # IN / OUT
    department = models.ForeignKey(Department, on_delete=models.PROTECT)
    remarks = models.TextField(blank=True)


# -----------------------------
# Attendance Management (Employee manages Attendance)
# -----------------------------
class AttendanceManagement(models.Model):
    manager = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='attendance_managed')
    attendance = models.ForeignKey(Attendance, on_delete=models.CASCADE, related_name='managed_by')
    reason = models.TextField()
    managed_at = models.DateTimeField(auto_now_add=True)


# -----------------------------
# Documents
# -----------------------------
class Document(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='documents')
    file_name = models.CharField(max_length=255)
    file_path = models.FileField(upload_to='documents/')
    created_at = models.DateTimeField(auto_now_add=True)


# -----------------------------
# Leave Policy
# -----------------------------
class LeavePolicy(models.Model):
    leave_type = models.CharField(max_length=100)
    number_of_days = models.IntegerField()
    eligibility = models.CharField(max_length=150)
    department_type = models.CharField(max_length=100)
    for_males = models.BooleanField(default=True)
    for_females = models.BooleanField(default=True)
    short_leave = models.BooleanField(default=False)
    long_leave = models.BooleanField(default=False)
    full_pay = models.BooleanField(default=True)
    half_pay = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.leave_type


# -----------------------------
# Leave Application
# -----------------------------
class LeaveApplication(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='leave_applications')
    leave_policy = models.ForeignKey(LeavePolicy, on_delete=models.PROTECT, related_name='applications')
    date = models.DateField()
    year = models.IntegerField()
    reason = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    leave_request_id = models.CharField(max_length=50, unique=True)
    approver = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, related_name='approved_leaves')
    apply_date = models.DateTimeField(auto_now_add=True)


# -----------------------------
# Leave Status
# -----------------------------
class LeaveStatus(models.Model):
    leave_application = models.ForeignKey(LeaveApplication, on_delete=models.CASCADE, related_name='statuses')
    current_approver = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, related_name='current_approvals')
    next_approver = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True, related_name='next_approvals')
    action = models.CharField(max_length=50)
    task_done_date = models.DateTimeField(auto_now_add=True)
    remarks = models.TextField(blank=True)
    leave_status = models.CharField(max_length=50)


# -----------------------------
# Notification
# -----------------------------
class Notification(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='notifications')
    leave_application = models.ForeignKey(LeaveApplication, on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
