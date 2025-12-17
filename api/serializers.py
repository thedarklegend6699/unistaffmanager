from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)

        # Add user data
        data['user'] = {
            "id": self.user.id,
            "email": self.user.email,
            "first_name": self.user.first_name,
            "last_name": self.user.last_name,
            "management_role": self.user.management_role,
            "employee_id": self.user.employee_id if self.user.employee else None
        }

        return data

from .models import (
    Department,
    Designation,
    Employee,
    User,
    Attendance,
    LeavePolicy,
    LeaveApplication,
    Notification
)

# -----------------------------
# Department Serializer
# -----------------------------
class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'


# -----------------------------
# Designation Serializer
# -----------------------------
class DesignationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Designation
        fields = '__all__'


# -----------------------------
# Employee Serializer
# -----------------------------
class EmployeeSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(
        source='department.department_name', read_only=True
    )
    designation_name = serializers.CharField(
        source='designation.designation_name', read_only=True
    )

    class Meta:
        model = Employee
        fields = '__all__'


# -----------------------------
# User Serializer
# -----------------------------
class UserSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer(read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'phone',
            'management_role',
            'employee'
        ]


# -----------------------------
# Attendance Serializer
# -----------------------------
class AttendanceSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(
        source='employee.employee_name', read_only=True
    )

    class Meta:
        model = Attendance
        fields = '__all__'


# -----------------------------
# Leave Policy Serializer
# -----------------------------
class LeavePolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = LeavePolicy
        fields = '__all__'


# -----------------------------
# Leave Application Serializer
# -----------------------------
class LeaveApplicationSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(
        source='employee.employee_name', read_only=True
    )
    leave_type = serializers.CharField(
        source='leave_policy.leave_type', read_only=True
    )

    class Meta:
        model = LeaveApplication
        fields = '__all__'


# -----------------------------
# Notification Serializer
# -----------------------------
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
