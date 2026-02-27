from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Employee, Education, Vehicle


# ======================
# ===== فرم کارمند =====
# ======================
class EmployeeForm(ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'
        widgets = {
            'hire_date': forms.TextInput(attrs={
                'placeholder': 'تاریخ استخدام (YYYY-MM-DD)'
            })
        }


# =======================
# ===== فرم تحصیلات =====
# =======================
class EducationForm(ModelForm):
    class Meta:
        model = Education
        exclude = ('employee',)


# =====================
# ===== فرم خودرو =====
# =====================
class VehicleForm(ModelForm):
    class Meta:
        model = Vehicle
        exclude = ('employee',)
        widgets = {
            'plate_number': forms.TextInput(attrs={
                'placeholder': 'سه رقم آخر پلاک'
            })
        }
        error_messages = {
            'plate_number': {
                'unique': 'این پلاک قبلاً ثبت شده است ❌'
            }
        }


# =============================
# ===== فرم ثبت نام درست =====
# =============================
class SignupForm(UserCreationForm):
    username = forms.CharField(label='نام کاربری')
    password1 = forms.CharField(
        label='رمز عبور',
        widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label='تکرار رمز عبور',
        widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


# ==========================
# ===== فرم لاگین فارسی =====
# ==========================
class LoginForm(AuthenticationForm):
    username = forms.CharField(label='نام کاربری')
    password = forms.CharField(
        label='رمز عبور',
        widget=forms.PasswordInput
    )