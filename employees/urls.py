
from django.urls import path
from .views import (
    EmployeeListView,
    EmployeeCreateView,
    EmployeeUpdateView,
    EmployeeDeleteView,
    EmployeePasswordChangeView,
    LoginUserView,
    LogoutUserView,
)

app_name = 'employees'

urlpatterns = [
    path('', LoginUserView.as_view(), name='login'),
    path('logout/', LogoutUserView.as_view(), name='logout'),
    path('list/', EmployeeListView.as_view(), name='employee-list'),
    path('create/', EmployeeCreateView.as_view(), name='employee-create'),
    path('employee/<int:pk>/edit/', EmployeeUpdateView.as_view(), name='employee-update'),
    path('employee/<int:pk>/delete/', EmployeeDeleteView.as_view(), name='employee-delete'),
    path('employee/<int:pk>/password/', EmployeePasswordChangeView.as_view(), name='employee-password-change'),
]