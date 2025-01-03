from django.db import models
from django.conf import settings


class WorkLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='work_logs', on_delete=models.PROTECT, verbose_name='کاربر')
    personnel_code = models.CharField(max_length=20, verbose_name="کد پرسنلی")
    time = models.TimeField(verbose_name="زمان")
    date = models.DateField(verbose_name="تاریخ")
    event_type = models.CharField(max_length=10, verbose_name="نوع رویداد",null=True,blank=True)
    device_id = models.CharField(max_length=10, null=True, blank=True, verbose_name="شناسه دستگاه")
    status = models.CharField(max_length=10, verbose_name="وضعیت",null=True, blank=True)

    def __str__(self):
        return f"{self.personnel_code} - {self.date} {self.time}"

    class Meta:
        verbose_name = "لاگ ورود و خروج"
        verbose_name_plural = "لاگ‌های ورود و خروج"
        constraints = [
            models.UniqueConstraint(
                fields=["personnel_code", "time", "date"], name="unique_attendance_log"
            )
        ]
