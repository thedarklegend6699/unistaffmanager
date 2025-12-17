# from django.core.management.base import BaseCommand
# from api.models import Designation, Department, LeavePolicy


# class Command(BaseCommand):
#     help = "Seed initial master data"

#     def handle(self, *args, **kwargs):

#         Designation.objects.get_or_create(designation_name="Assistant Professor", scale="18th", status=True)
#         Designation.objects.get_or_create(designation_name="Professor", scale="17th", status=True)
#         Designation.objects.get_or_create(designation_name="Lecturer", scale="18th", status=True)
#         Designation.objects.get_or_create(designation_name="HR Manager", scale="17th", status=True)
#         Designation.objects.get_or_create(designation_name="Developer", scale="17th", status=True)
#         Designation.objects.get_or_create(designation_name="Head Of Department", scale="19th", status=True)
#         Designation.objects.get_or_create(designation_name="InCharge Campus", scale="20th", status=True)
#         Designation.objects.get_or_create(designation_name="Vice Chancellor", scale="20th", status=True)
#         Designation.objects.get_or_create(designation_name="Registrar", scale="19th", status=True)

#         Department.objects.get_or_create(department_type="Academic", department_name="Computer Science")
#         Department.objects.get_or_create(department_type="Academic", department_name="Applied Physics")
#         Department.objects.get_or_create(department_type="Academic", department_name="English")
#         Department.objects.get_or_create(department_type="Administrative", department_name="IT")
#         Department.objects.get_or_create(department_type="Administrative", department_name="Human Resources")
#         Department.objects.get_or_create(department_type="Administrative", department_name="Department Of Administration")
#         Department.objects.get_or_create(department_type="Management", department_name="Department Of Management")

#         LeavePolicy.objects.bulk_create([
#             LeavePolicy(leave_type="Earned Leave", number_of_days=3, eligibility="Faculty", department_type="Academic", for_males=1, for_females=1, short_leave=0, long_leave=1, full_pay=0, half_pay=0, is_active=1),
#             LeavePolicy(leave_type="Earned Leave", number_of_days=4, eligibility="Non-Faculty", department_type="Administrative", for_males=1, for_females=1, short_leave=0, long_leave=1, full_pay=0, half_pay=0, is_active=1),
#             LeavePolicy(leave_type="Casual Leave", number_of_days=20, eligibility="For All Employees", department_type="For All Department Types", for_males=1, for_females=1, short_leave=1, long_leave=1, full_pay=0, half_pay=0, is_active=1),
#             LeavePolicy(leave_type="Sick Leave", number_of_days=365, eligibility="For All Employees", department_type="For All Department Types", for_males=1, for_females=1, short_leave=0, long_leave=1, full_pay=0, half_pay=1, is_active=1),
#             LeavePolicy(leave_type="Study Leave", number_of_days=1460, eligibility="Faculty", department_type="Academic", for_males=1, for_females=1, short_leave=0, long_leave=1, full_pay=0, half_pay=0, is_active=1),
#             LeavePolicy(leave_type="Maternity Leave", number_of_days=92, eligibility="For All Employees", department_type="For All Department Types", for_males=0, for_females=1, short_leave=0, long_leave=1, full_pay=0, half_pay=0, is_active=1),
#             LeavePolicy(leave_type="Duty Leave", number_of_days=0, eligibility="For All Employees", department_type="For All Department Types", for_males=1, for_females=1, short_leave=0, long_leave=1, full_pay=0, half_pay=0, is_active=1),
#             LeavePolicy(leave_type="Disability Leave", number_of_days=182, eligibility="For All Employees", department_type="For All Department Types", for_males=1, for_females=1, short_leave=0, long_leave=1, full_pay=0, half_pay=0, is_active=1),
#             LeavePolicy(leave_type="Extraordinary Leave", number_of_days=2190, eligibility="For All Employees", department_type="For All Department Types", for_males=1, for_females=1, short_leave=0, long_leave=1, full_pay=0, half_pay=0, is_active=1),
#             LeavePolicy(leave_type="Special Leave", number_of_days=62, eligibility="For All Employees", department_type="For All Department Types", for_males=1, for_females=1, short_leave=0, long_leave=1, full_pay=0, half_pay=0, is_active=1),
#             LeavePolicy(leave_type="Foreign Service Leave", number_of_days=2190, eligibility="Faculty", department_type="Academic", for_males=1, for_females=1, short_leave=0, long_leave=1, full_pay=0, half_pay=0, is_active=1),
#             LeavePolicy(leave_type="Foreign Service Leave", number_of_days=2190, eligibility="Non-Faculty", department_type="Administrative", for_males=1, for_females=1, short_leave=0, long_leave=1, full_pay=0, half_pay=0, is_active=1),
#             LeavePolicy(leave_type="Sabbatical Leave", number_of_days=273, eligibility="Faculty", department_type="Academic", for_males=1, for_females=1, short_leave=0, long_leave=1, full_pay=1, half_pay=1, is_active=1),
#             LeavePolicy(leave_type="Summer Leave", number_of_days=92, eligibility="Faculty", department_type="Academic", for_males=1, for_females=1, short_leave=0, long_leave=1, full_pay=0, half_pay=0, is_active=1),
#             LeavePolicy(leave_type="Summer Leave", number_of_days=92, eligibility="For All Employees", department_type="Management", for_males=1, for_females=1, short_leave=0, long_leave=1, full_pay=0, half_pay=0, is_active=1),
#         ])

#         self.stdout.write(self.style.SUCCESS("Master data seeded successfully"))
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from api.models import (
    Department,
    Designation,
    Employee,
    EmployeeManagement,
    EmployeeJobHistory,
    Attendance,
    AttendanceManagement,
    Document,
    LeavePolicy,
    LeaveApplication,
    LeaveStatus,
    Notification
)
from datetime import date, time


class Command(BaseCommand):
    help = "Seed one record for all core tables"

    def handle(self, *args, **kwargs):

        User = get_user_model()

        # -------------------------------------------------
        # REQUIRED MASTER DATA (ASSUMED TO EXIST)
        # -------------------------------------------------
        department = Department.objects.first()
        designation = Designation.objects.first()
        leave_policy = LeavePolicy.objects.first()

        if not department or not designation or not leave_policy:
            self.stdout.write(self.style.ERROR(
                "Department, Designation, and LeavePolicy must exist before running this seed."
            ))
            return

        # -------------------------------------------------
        # EMPLOYEE
        # -------------------------------------------------
        employee, _ = Employee.objects.get_or_create(
            cnic="12345-1234567-1",
            defaults={
                "employee_name": "Ali Khan",
                "father_name": "Ahmed Khan",
                "gender": "Male",
                "designation": designation,
                "department": department,
                "domicile": "Punjab",
                "date_of_birth": date(1990, 1, 1),
                "date_of_joining": date(2020, 1, 1),
                "qualification": "MS Computer Science",
                "research_paper": "AI Research",
                "experience": 5,
                "leave_balance": 20,
            }
        )

        # -------------------------------------------------
        # USER (LINKED TO EMPLOYEE)
        # -------------------------------------------------
        if not User.objects.filter(email="admin@university.com").exists():
            user = User.objects.create_superuser(
                email="admin@university.com",
                password="admin123",
                first_name="System",
                last_name="Admin",
                phone="03001234567",
                employee=employee,
                management_role="Administrator"
            )
        else:
            user = User.objects.get(email="admin@university.com")

        # -------------------------------------------------
        # EMPLOYEE MANAGEMENT
        # -------------------------------------------------
        EmployeeManagement.objects.get_or_create(
            manager=employee,
            employee=employee,
            defaults={"reason": "Initial assignment"}
        )

        # -------------------------------------------------
        # EMPLOYEE JOB HISTORY
        # -------------------------------------------------
        EmployeeJobHistory.objects.get_or_create(
            employee=employee,
            start_date=date(2020, 1, 1),
            defaults={
                "description": "Joined as faculty member",
                "end_date": None
            }
        )

        # -------------------------------------------------
        # ATTENDANCE
        # -------------------------------------------------
        attendance, _ = Attendance.objects.get_or_create(
            employee=employee,
            attendance_date=date.today(),
            defaults={
                "attendance_time": time(9, 0),
                "direction": "IN",
                "department": department,
                "remarks": "On time"
            }
        )

        # -------------------------------------------------
        # ATTENDANCE MANAGEMENT
        # -------------------------------------------------
        AttendanceManagement.objects.get_or_create(
            manager=employee,
            attendance=attendance,
            defaults={"reason": "Auto approval"}
        )

        # -------------------------------------------------
        # DOCUMENT
        # -------------------------------------------------
        Document.objects.get_or_create(
            employee=employee,
            file_name="appointment_letter.pdf",
            defaults={
                "file_path": "documents/appointment_letter.pdf"
            }
        )

        # -------------------------------------------------
        # LEAVE APPLICATION
        # -------------------------------------------------
        leave_application, _ = LeaveApplication.objects.get_or_create(
            leave_request_id="LR-0001",
            defaults={
                "employee": employee,
                "leave_policy": leave_policy,
                "date": date.today(),
                "year": date.today().year,
                "reason": "Medical leave",
                "start_date": date.today(),
                "end_date": date.today(),
                "approver": employee
            }
        )

        # -------------------------------------------------
        # LEAVE STATUS
        # -------------------------------------------------
        LeaveStatus.objects.get_or_create(
            leave_application=leave_application,
            current_approver=employee,
            defaults={
                "next_approver": None,
                "action": "Approved",
                "remarks": "Approved by system",
                "leave_status": "Approved"
            }
        )

        # -------------------------------------------------
        # NOTIFICATION
        # -------------------------------------------------
        Notification.objects.get_or_create(
            employee=employee,
            leave_application=leave_application,
            defaults={
                "message": "Your leave has been approved",
                "is_read": False
            }
        )

        self.stdout.write(self.style.SUCCESS("All core tables seeded successfully."))
