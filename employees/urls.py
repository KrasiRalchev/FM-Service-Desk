
from django.urls import path
from .views import (
    EmployeeListView,
    EmployeeCreateView,
    EmployeeUpdateView,
    EmployeeDeleteView,
    EmployeePasswordChangeView,
)

app_name = 'employees'

urlpatterns = [
    path('', EmployeeListView.as_view(), name='employee_list'),
    path('create/', EmployeeCreateView.as_view(), name='employee_create'),
    path('employee/<int:pk>/edit/', EmployeeUpdateView.as_view(), name='employee_update'),
    path('employee/<int:pk>/delete/', EmployeeDeleteView.as_view(), name='employee_delete'),
    path('employee/<int:pk>/password/', EmployeePasswordChangeView.as_view(), name='employee_password_change'),
]