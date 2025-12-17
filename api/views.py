from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import (
    Department,
    Designation,
    Employee,
    Attendance,
    LeavePolicy,
    LeaveApplication,
    Notification
)

from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer

class CustomLoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


from .serializers import (
    DepartmentSerializer,
    DesignationSerializer,
    EmployeeSerializer,
    AttendanceSerializer,
    LeavePolicySerializer,
    LeaveApplicationSerializer,
    NotificationSerializer
)


# -----------------------------
# Department API
# -----------------------------
class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]


# -----------------------------
# Designation API
# -----------------------------
class DesignationViewSet(viewsets.ModelViewSet):
    queryset = Designation.objects.all()
    serializer_class = DesignationSerializer
    permission_classes = [IsAuthenticated]


# -----------------------------
# Employee API
# -----------------------------
class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]


# -----------------------------
# Attendance API
# -----------------------------
class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]


# -----------------------------
# Leave Policy API
# -----------------------------
class LeavePolicyViewSet(viewsets.ModelViewSet):
    queryset = LeavePolicy.objects.all()
    serializer_class = LeavePolicySerializer
    permission_classes = [IsAuthenticated]


# -----------------------------
# Leave Application API
# -----------------------------
class LeaveApplicationViewSet(viewsets.ModelViewSet):
    queryset = LeaveApplication.objects.all()
    serializer_class = LeaveApplicationSerializer
    permission_classes = [IsAuthenticated]


# -----------------------------
# Notification API
# -----------------------------
class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
