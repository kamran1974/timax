from persiantools.jdatetime import JalaliDate

def convert_jalali_date_to_gregorian(date_str):
    if '-' in date_str:
        year, month, day = map(int, date_str.split('-'))
        return JalaliDate.to_jalali(year, month, day)

    year, month, day = map(int, date_str.split('/'))

    return JalaliDate(year, month, day).to_gregorian()


def convert_second_to_hour(second):
    hours, remainder = divmod(second, 3600)
    minutes, _ = divmod(remainder, 60)

    return f'{int(hours)}:{int(minutes)}'
