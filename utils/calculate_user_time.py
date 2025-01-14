from datetime import timedelta

from inout.models import WorkLog
from utils.calculate_date import convert_jalali_date_to_gregorian, convert_second_to_hour
from utils.day_generator import generate_empty_data, get_date_range


def calculate_user_logs(user_id, start_date, end_date):
    days =(end_date - start_date).days

    if days >90:
        return 'errore',('حداکثر بازه مجاز ۹۰ روز می باشد')

    # personnel_code='0000000001',#0000000001, 0000000620, 0000000820, 0000000036
    logs = WorkLog.objects.filter(
        user_id=user_id,
        # personnel_code='0000000001',
        date__range=(start_date, end_date)
    ).order_by('date', 'time')

    if not logs.exists():
        return {"message": "No logs found for this user in the given date range."}

    daily_logs = {}
    for log in logs:
        jalili_date = convert_jalali_date_to_gregorian(str(log.date))
        daily_logs[jalili_date] = daily_logs.get(jalili_date,
                                                 {'entries': []
                                                     ,'exits': []
                                                     , 'login':True
                                                     , 'total_stay':timedelta(0)
                                                     , 'fail':False
                                                     , 'work_hours':''
                                                     ,'sum_works':timedelta(0)
                                                     ,'status':'غایب'
                                                     ,'karkard':0
                                                  }) #login for insert data

        if daily_logs[jalili_date]['login']:
            daily_logs[jalili_date]['entries'].append(log.time)
            daily_logs[jalili_date]['login'] = False
        else:
            daily_logs[jalili_date]['exits'].append(log.time)
            daily_logs[jalili_date]['login'] = True

    total_month_hour = timedelta(0)
    for date_str, data in daily_logs.items():
        entries = data['entries']
        exits = data['exits']

        data['sum_taradods'] = min([len(entries), len(exits)],default=0)

        if len(entries) !=  len(exits):
            daily_logs[date_str]['fail'] = True
            data['status'] = 'حضور ناقص'
            data['karkard'] = 0
            continue
        else:
            if len(entries) == len(exits):
                if exits:
                    data['status'] = 'حاضر'
                    data['karkard'] =1
                else:
                    data['status'] = 'غایب'
                    data['karkard'] = 0
            for entry_time, exit_time in zip(entries, exits):
                entry = timedelta(hours=entry_time.hour, minutes=entry_time.minute, seconds=entry_time.second)
                exit = timedelta(hours=exit_time.hour, minutes=exit_time.minute, seconds=exit_time.second)
                data['total_stay'] += exit - entry
            total_month_hour += data['total_stay']
            data['work_hours'] = str(data['total_stay'])


    date_range = get_date_range(str(start_date), str(end_date))
    daily_log = generate_empty_data(date_range)

    for day in daily_log:
        if day not in daily_logs:
            daily_logs[day] = daily_log[day]

    daily_logs = dict(sorted(daily_logs.items(), key=lambda item: item[0]))
    daily_logs['total_month_hour'] = total_month_hour

    return daily_logs




def calculate_user_log_to_list(user_log:dict) -> list:
    result = []
    last_row = []
    total_month_hour = convert_second_to_hour(user_log.pop('total_month_hour').total_seconds())
    __sum_karkard = 0
    extra_data = dict(total_month_hour=total_month_hour)
    weekday_translation = {
        0: "شنبه",
        1: "یکشنبه",
        2: "دوشنبه",
        3: "سه‌شنبه",
        4: "چهارشنبه",
        5: "پنج‌شنبه",
        6: "جمعه"
    }

    for date, data in user_log.items():
        row = []
        try:
            year = date.year
            month = date.month
            day = date.day
        except Exception as e:
            print('error: date')
        date_fa = f"{year}/{month}/{day}"

        weekday_fa = weekday_translation.get(date.weekday(), "نامشخص")

        entries = data['entries']
        exits = data['exits']

        entries_length = len(entries)
        exits_length = len(exits)


        status = data['status']
        karkard = data['karkard']
        __sum_karkard += karkard

        if exits_length  == 0:
            first_entire = ''
        else:
            first_entire = entries[0]

        if entries_length == 0:
            exsist_last = ''
        else:
            exsist_last = exits[-1] if len(exits) !=0 else ''

        if entries_length <3:
            space = 3 - entries_length
            entries += [''] * space
        if exits_length <3:
            space = 3 - exits_length
            exits += [''] * space



        tr1 = entries[0]
        tr2 = exits[0]

        tr3 = entries[1]
        tr4 = exits[1]

        tr5 = entries[2]
        tr6 = exits[2]

        sum_taradods = data['sum_taradods']

        work_hours = data['work_hours']


        row.extend([date_fa, weekday_fa, tr1, tr2, tr3, tr4, tr5, tr6, sum_taradods,first_entire, exsist_last, work_hours,'0','0','0',karkard, status])
        result.append(list(reversed(row)))

    extra_data['sum_karkard'] = __sum_karkard

    return result, extra_data

# from datetime import date
#
# user_id = 1
# start_date = date(2024, 12, 1)
# end_date = date(2024, 12, 30)
#from datetime import date;user_id = 1;start_date = date(2021, 9, 23);end_date = date(2021, 10, 20);from utils.calculate_user_time import calculate_user_logs,calculate_user_log_to_list
#from utils.calculate_user_time import calculate_user_logs
#'2021-9-23','2021-10-20'
# result = calculate_user_logs(user_id, start_date, end_date)


