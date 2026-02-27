from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse_lazy

from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.views import LoginView

from .models import Employee, Education, Vehicle
from .forms import EmployeeForm, EducationForm, VehicleForm, LoginForm, SignupForm


# --------------------------------------------------
# Public Pages
# --------------------------------------------------

def landing(request):
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'landing.html')


# --------------------------------------------------
# Dashboard
# --------------------------------------------------

@login_required
def home(request):
    qs = Employee.objects.all()

    return render(request, 'home.html', {
        'employees': qs,
        'total_employees': qs.count(),
        'active_employees': qs.filter(is_active=True).count(),
        'inactive_employees': qs.filter(is_active=False).count(),
    })


# --------------------------------------------------
# Authentication
# --------------------------------------------------

def signup(request):
    if request.user.is_authenticated:
        return redirect('home')

    form = SignupForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, 'ثبت‌نام با موفقیت انجام شد ✅')
        return redirect('home')

    return render(request, 'signup.html', {'form': form})


class CustomLoginView(LoginView):
    template_name = 'login.html'
    authentication_form = LoginForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        messages.success(self.request, 'با موفقیت وارد شدید ✅')
        return super().form_valid(form)


# --------------------------------------------------
# Employee CRUD
# --------------------------------------------------

@login_required
def add(request):
    emp_form = EmployeeForm(request.POST or None, request.FILES or None)
    edu_form = EducationForm(request.POST or None)
    veh_form = VehicleForm(request.POST or None)

    if emp_form.is_valid() and edu_form.is_valid() and veh_form.is_valid():
        employee = emp_form.save()

        education = edu_form.save(commit=False)
        education.employee = employee
        education.save()

        vehicle = veh_form.save(commit=False)
        vehicle.employee = employee
        vehicle.save()

        messages.success(request, 'اطلاعات با موفقیت ثبت شد ✅')
        return redirect('home')

    return render(request, 'form.html', {
        'emp_form': emp_form,
        'edu_form': edu_form,
        'veh_form': veh_form,
    })


@login_required
def edit(request, id):
    employee = get_object_or_404(Employee, pk=id)

    emp_form = EmployeeForm(request.POST or None, request.FILES or None, instance=employee)
    edu_form = EducationForm(
        request.POST or None,
        instance=Education.objects.filter(employee=employee).first()
    )
    veh_form = VehicleForm(
        request.POST or None,
        instance=Vehicle.objects.filter(employee=employee).first()
    )

    if emp_form.is_valid() and edu_form.is_valid() and veh_form.is_valid():
        emp_form.save()

        education = edu_form.save(commit=False)
        education.employee = employee
        education.save()   # ✅ این خط مشکل‌دار بود

        vehicle = veh_form.save(commit=False)
        vehicle.employee = employee
        vehicle.save()

        messages.success(request, 'ویرایش با موفقیت انجام شد ✏️')
        return redirect('home')

    return render(request, 'form.html', {
        'emp_form': emp_form,
        'edu_form': edu_form,
        'veh_form': veh_form,
    })


@login_required
def delete(request, id):
    employee = get_object_or_404(Employee, pk=id)
    employee.delete()
    messages.success(request, 'کارمند حذف شد 🗑')
    return redirect('home')