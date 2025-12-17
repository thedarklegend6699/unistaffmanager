from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import (
    DepartmentViewSet,
    DesignationViewSet,
    EmployeeViewSet,
    AttendanceViewSet,
    LeavePolicyViewSet,
    LeaveApplicationViewSet,
    NotificationViewSet,
    CustomLoginView
)

# DRF Router
router = DefaultRouter()
router.register(r'departments', DepartmentViewSet)
router.register(r'designations', DesignationViewSet)
router.register(r'employees', EmployeeViewSet)
router.register(r'attendance', AttendanceViewSet)
router.register(r'leave-policies', LeavePolicyViewSet)
router.register(r'leave-applications', LeaveApplicationViewSet)
router.register(r'notifications', NotificationViewSet)


urlpatterns = [
    path('api/', include(router.urls)),
    path('api/login/', CustomLoginView.as_view(), name='login'),
]
