from uuid import uuid4

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    personnel_code = models.CharField(max_length=128, unique=True, verbose_name="کد پرسنلی", default=uuid4)
    DEPARTMENT_CHOICES = [
        ('technical', 'فنی'),
        ('services', 'خدمات'),
        ('other', 'سایر'),
    ]
    department = models.CharField(max_length=20, choices=DEPARTMENT_CHOICES, verbose_name="بخش فعالیت", null=True, blank=True)

    marital_status = models.BooleanField(default=False, verbose_name="وضعیت تأهل (مجرد/متأهل)")
    children_count = models.PositiveIntegerField(default=0, verbose_name="تعداد فرزند")
    hire_date = models.DateField(verbose_name="تاریخ استخدام", null=True, blank=True)

    EMPLOYMENT_TYPE_CHOICES = [
        ('hourly', 'ساعتی'),
        ('contract', 'قراردادی'),
    ]
    employment_type = models.CharField(max_length=20, choices=EMPLOYMENT_TYPE_CHOICES, verbose_name="نوع استخدام",blank=True,null=True)


    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.personnel_code})"
