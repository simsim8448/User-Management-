from django.db import models


class Employee(models.Model):
    first_name = models.CharField(max_length=50, verbose_name='نام')
    last_name = models.CharField(max_length=50, verbose_name='نام خانوادگی')
    national_code = models.CharField(max_length=10, unique=True, verbose_name='کد ملی')
    phone_number = models.CharField(max_length=11, verbose_name='شماره تماس')
    address = models.TextField(verbose_name='آدرس')
    hire_date = models.DateField(
        verbose_name='تاریخ استخدام',
        help_text='تاریخ استخدام را به فرمت میلادی وارد کنید (YYYY-MM-DD)'
    )
    photo = models.ImageField(upload_to='employees/', blank=True, null=True, verbose_name='عکس')
    is_active = models.BooleanField(default=True, verbose_name='فعال')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Education(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='educations')
    degree = models.CharField(max_length=50, verbose_name='مقطع تحصیلی')
    field_of_study = models.CharField(max_length=100, verbose_name='رشته تحصیلی')
    university = models.CharField(max_length=100, verbose_name='دانشگاه')
    graduation_year = models.IntegerField(verbose_name='سال فارغ‌التحصیلی')

    def __str__(self):
        return f'{self.degree} - {self.employee}'


class Vehicle(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='vehicles')
    plate_number = models.CharField(
        max_length=3,
        unique=True,
        verbose_name='پلاک خودرو',
        help_text='سه رقم آخر پلاک را وارد کنید'
    )

    def __str__(self):
        return self.plate_number