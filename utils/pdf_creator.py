from fpdf import FPDF
from arabic_reshaper import reshape
from bidi.algorithm import get_display
from datetime import datetime
from io import BytesIO
from persiantools.jdatetime import JalaliDate

from account.models import User
from utils.calculate_user_time import calculate_user_logs, calculate_user_log_to_list


class PDF(FPDF):
    def __init__(self, user):
        super().__init__()
        import os
        self.user = User.objects.get(id=user)
        font_path = os.path.join(os.path.dirname(__file__), "Vazirmatn-Regular.ttf")
        font_path2 = os.path.join(os.path.dirname(__file__), "Vazirmatn-Bold.ttf")


        self.add_font('Vazir', '', font_path, uni=True)
        self.add_font('Vazir', 'B', font_path2, uni=True)
        self.base_data()

    def header(self):
        # هدر گزارش
        self.set_font('Vazir', 'B', 10)  # فونت برای عنوان اصلی
        title = get_display(reshape('گزارش انفرادی'))
        self.cell(0, 10, title, align='C', ln=1)
        self.ln(5)

        # اطلاعات تاریخ و ساعت
        self.set_font('Vazir', '', 8)  # فونت کوچکتر برای تاریخ و ساعت
        date = get_display(reshape('تاریخ گزارشگیری: '+f'{self.current_date}')) #+
        time = get_display(reshape('ساعت گزارشگیری: '+f'{self.current_time}')) #+

        # تنظیم مکان تاریخ و ساعت
        self.cell(0, 10, date, align='R', ln=0)  # تاریخ سمت راست
        self.cell(-150)  # ایجاد فاصله مناسب
        self.cell(0, 10, time, align='L', ln=1)  # ساعت سمت چپ
        self.ln(5)

        # مشخصات فردی
        self.set_font('Vazir', '', 8)
        self.cell(0, 10, get_display(reshape('نام و نام خانوادگی: '+f'{self.full_name}')), align='R', ln=0)
        self.cell(-135)
        self.cell(0, 10, get_display(reshape('شماره کارت:'+f'{self.user_code}')), align='L', ln=1)
        self.cell(0, 10, get_display(reshape('گروه کاری: '+f'{self.user.department}')), align='R', ln=0)
        self.cell(-135)
        self.cell(0, 10, get_display(reshape('شماره پرسنلی: '+f'{self.user.personnel_code}')), align='L', ln=1)
        self.ln(10)

    def footer(self):
        # فوتر
        self.set_y(-15)
        self.set_font('Vazir', '', 7)  # فونت کوچکتر
        footer_text = get_display(reshape(f'صفحه {self.page_no()}'))
        self.cell(0, 10, footer_text, align='C')


    def base_data(self):
        now = datetime.now()
        self.full_name = self.user.get_full_name()
        self.current_date = str(JalaliDate(now).strftime('%Y/%m/%d'))
        self.current_time = now.strftime('%I:%M %p')
        self.current_time = str(self.current_time.replace('AM', 'ق.ظ').replace('PM', 'ب.ظ'))
        self.user_code = self.user.personnel_code


def create_report(_user, start_date, end_date):
    pdf = PDF(user=_user)

    # تنظیم اندازه صفحه A4 (عرض 210mm و ارتفاع 297mm)
    pdf.add_page(format='A4')

    data,extra_data = calculate_user_log_to_list(calculate_user_logs(_user, start_date, end_date))

    # تنظیم فونت برای جدول (کوچکتر از هدر)
    pdf.set_font('Vazir', '', 5)

    # طراحی جدول
    column_widths = [12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12]
    headers = ['وضعیت', 'کارکرد', 'تعطیل کاری', 'ماموریت روزانه', 'مرخصی روزانه', 'حضور', 'خروج', 'ورود', 'ترددها', 'تردد۶', 'تردد۵', 'تردد۴', 'تردد۳', 'تردد۲', 'تردد۱', 'روز', 'تاریخ']

    reshaped_headers = [get_display(reshape(header)) for header in headers]

    # هدر جدول
    pdf.set_fill_color(200, 220, 255)
    total_width = sum(column_widths)  # مجموع عرض ستون‌ها
    pdf.set_x((210 - total_width) / 2)  # تنظیم فاصله برای اینکه جدول وسط صفحه باشد
    for header, width in zip(reshaped_headers, column_widths):
        pdf.cell(width, 6, header, border=1, align='C', fill=True)
    pdf.ln()

    # ردیف‌های جدول
    fill = False
    for row in data:
        reshaped_row = [get_display(reshape(str(item))) for item in row]

        pdf.set_x((210 - total_width) / 2)
        for item, width in zip(reshaped_row, column_widths):
            pdf.cell(width, 5, item, border=1, align='C', fill=fill)
        pdf.ln()
        fill = not fill

    ############Section new
    pdf.set_fill_color(220, 230, 240)

    pdf.set_x((210 - total_width) / 2)

    pdf.cell(12 , 5, '', border=1, align='C', fill=True)
    pdf.cell(12 , 5, f'{extra_data["sum_karkard"]}', border=1, align='C', fill=True)
    pdf.cell(12 , 5, '', border=1, align='C', fill=True)
    pdf.cell(12 , 5, '', border=1, align='C', fill=True)
    pdf.cell(12 , 5, '', border=1, align='C', fill=True)
    pdf.cell(12 , 5, f'{extra_data["total_month_hour"]}', border=1, align='C', fill=True)
    pdf.cell(12 * 2, 5, '', border=1, align='C', fill=True)
    pdf.cell(12 * 7, 5, get_display(reshape('ترددها')), border=1, align='C', fill=True)
    pdf.cell(12 * 2, 5, get_display(reshape('سرجمع')), border=1, align='C', fill=True)
    pdf.ln()








    buffer = BytesIO()

    # pdf.output('jadid.pdf')
    pdf.output(buffer)
    buffer.seek(0)

    return buffer




