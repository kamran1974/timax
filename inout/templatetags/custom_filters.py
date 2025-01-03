from django import template

register = template.Library()

weekday_translation = {
    0: "شنبه",
    1: "یکشنبه",
    2: "دوشنبه",
    3: "سه‌شنبه",
    4: "چهارشنبه",
    5: "پنج‌شنبه",
    6: "جمعه"
}

@register.filter
def format_date_fa(date):
    print(date, type(date))
    try:
        year = date.year
        month = date.month
        day = date.day
    except AttributeError:
        return "تاریخ نامعتبر"

    date_fa = f"{year}-{month}-{day}"
    weekday_fa = weekday_translation.get(date.weekday(), "نامشخص")
    return f"{date_fa} / {weekday_fa}"
