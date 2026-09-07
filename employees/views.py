
# main role - users and authorization

from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.mixins import StaffRequiredMixin
from .forms import EmployeeCreateForm, EmployeeUpdateForm
from .models import UserProfile
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.views.generic import FormView
from .forms import EmployeePasswordChangeForm


from django.db.models import Q

class EmployeeListView(StaffRequiredMixin, ListView):
    model = UserProfile
    template_name = 'employees/employee_list.html'
    context_object_name = 'employees'
    ordering = ['last_name', 'first_name']
    paginate_by = 20  # по желание

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('q')
        department = self.request.GET.get('department')

        if q:
            queryset = queryset.filter(
                Q(first_name__icontains=q) |
                Q(last_name__icontains=q) |
                Q(position__icontains=q) |
                Q(phone__icontains=q) |
                Q(user__username__icontains=q)
            )

        if department:
            queryset = queryset.filter(department__icontains=department)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '')
        context['department'] = self.request.GET.get('department', '')
        return context


class EmployeeCreateView(StaffRequiredMixin, CreateView):
    model = UserProfile
    form_class = EmployeeCreateForm
    template_name = 'employees/employee_form.html'
    success_url = reverse_lazy('employees:employee_list')


class EmployeeUpdateView(StaffRequiredMixin, UpdateView):
    model = UserProfile
    form_class = EmployeeUpdateForm
    template_name = 'employees/employee_form.html'
    success_url = reverse_lazy('employees:employee_list')


class EmployeeDeleteView(StaffRequiredMixin, DeleteView):
    model = UserProfile
    template_name = 'employees/employee_confirm_delete.html'
    success_url = reverse_lazy('employees:employee_list')

    def delete(self, request, *args, **kwargs):
        # Изтриваме и User-а заедно с Profile-а
        profile = self.get_object()
        user = profile.user
        response = super().delete(request, *args, **kwargs)
        user.delete()
        return response


class EmployeePasswordChangeView(StaffRequiredMixin, FormView):
    template_name = 'employees/employee_password_change.html'
    form_class = EmployeePasswordChangeForm
    success_url = reverse_lazy('employees:employee_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        self.user = get_object_or_404(User, profile__pk=self.kwargs['pk'])
        kwargs['user'] = self.user
        return kwargs

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['employee'] = self.user.profile
        return context