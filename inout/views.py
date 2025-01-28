from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse
from account.models import User

import csv
from persiantools.jdatetime import JalaliDate
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.views.generic import ListView

from utils.calculate_user_time import calculate_user_logs
from utils.calculate_date import convert_jalali_date_to_gregorian, convert_second_to_hour
from inout.forms import CSVUploadForm
from inout.models import WorkLog
from utils.pdf_creator import create_report


def is_superuser(user):
    return user.is_superuser

def check_user_exists(users_list):
    """
        USAGE: in upload work_log file users
    """
    errors = []
    for row in users_list:
        try:
            personnel_code=row[0].strip()
            User.objects.get(personnel_code=personnel_code)
        except:
            errors.append(f'کاربری با این {personnel_code}شناسه وجود ندارد'+'\n')

    return errors


@user_passes_test(is_superuser, login_url='account:login_page')
def upload_worklog(request):
    if request.method == "POST":
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES["file"]
            try:
                decoded_file = file.read().decode("utf-8-sig").splitlines()
                csv_reader = csv.reader(decoded_file)
                csv_data = list(csv_reader)
                
                users_map = {user.personnel_code: user for user in User.objects.all()}
                
                csv_personnel_codes = {row[0].strip() for row in csv_data}
                invalid_codes = csv_personnel_codes - set(users_map.keys())
                if invalid_codes:
                    for code in invalid_codes:
                        messages.error(request, f"کاربر با کد پرسنلی {code} یافت نشد.")
                    return redirect("inout:upload_worklog")  
                
                worklogs = []
                for row in csv_data:
                    try:
                        personnel_code = row[0].strip()
                        time = row[1].strip()
                        year, month, day = map(int, row[2].strip().split('/'))
                        event_type = row[3].strip()
                        device_id = row[4].strip()
                        status = row[5].strip()

                        gregorian_date = JalaliDate(year, month, day).to_gregorian()
                        user = users_map.get(personnel_code)

                        worklogs.append(WorkLog(
                            user=user,
                            personnel_code=personnel_code,
                            time=time,
                            date=gregorian_date,
                            event_type=event_type,
                            device_id=device_id,
                            status=status,
                        ))
                    except Exception as e:
                        messages.warning(request, f"خطا در پردازش ردیف {row}: {e}")
                
                WorkLog.objects.bulk_create(worklogs,  ignore_conflicts=True)
                messages.success(request, "فایل با موفقیت آپلود و پردازش شد.")
            except Exception as e:
                messages.error(request, f"خطا در پردازش فایل: {e}")
        else:
            messages.error(request, "فرم معتبر نیست. لطفاً دوباره تلاش کنید.")
    else:
        form = CSVUploadForm()

    return render(request, "inout/upload_worklog.html", {"form": form})





class WorkLogReportView(LoginRequiredMixin, ListView):
    model = WorkLog
    template_name = "inout/report_home.html"

    context_object_name = "logs"
    paginate_by = 10


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = get_user_model().objects.all()

        user       = self.request.user
        end_date   = self.request.GET.get("end_date", "")
        start_date = self.request.GET.get("start_date", "")

        if user.is_staff:
            user = self.request.GET.get("user", "")
        else:
            user = user.id

        if start_date and end_date and user:
            print(user)
            start_date = convert_jalali_date_to_gregorian(start_date)
            end_date = convert_jalali_date_to_gregorian(end_date)
            data = calculate_user_logs(user, start_date, end_date)

            if 'total_month_hour' in data:
                context['total_month_hour'] = convert_second_to_hour(data.pop('total_month_hour').total_seconds())

            if 'errore' in data:
                messages.error(self.request, data[1])

            if 'message' not in data:
                sum_karkard = 0
                for date,value in data.items():
                    sum_karkard += value['karkard']
                context['sum_karkard'] = sum_karkard
                context['user_data'] = data

        return context



def generate_pdf(request):
    try:
        user_id = request.GET.get("user")
        start_date = convert_jalali_date_to_gregorian(request.GET.get("start_date"))
        end_date = convert_jalali_date_to_gregorian(request.GET.get("end_date"))

        buffer = create_report(user_id, start_date, end_date)

        response = HttpResponse(buffer, content_type="application/pdf")
        response["Content-Disposition"] = f"attachment; filename=report_{user_id}_{start_date}_{end_date}.pdf"
        return response
    except:
        messages.error(request, "خطایی در تولید گزارش رخ داد. لطفاً دوباره تلاش کنید.")
        return redirect("inout:worklog_report")
