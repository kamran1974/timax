from datetime import datetime, timedelta
from utils.calculate_date import convert_jalali_date_to_gregorian

def get_date_range(start_date, end_date):
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")

    date_range = []
    while start <= end:
        date_range.append(start.strftime("%Y-%m-%d"))
        start += timedelta(days=1)

    return date_range


def generate_empty_data(date_range):

    result = dict()
    default_data = {'entries': []
                     ,'exits': []
                     , 'login':True
                     , 'total_stay':timedelta(0)
                     , 'fail':False
                     , 'work_hours':''
                     ,'sum_taradods': 0
                     ,'status':'غایب'
                     ,'karkard':0
                  }

    for i in date_range:
        day = convert_jalali_date_to_gregorian(i)
        result[day] = default_data

    return result


# start_date = "2023-01-01"
# end_date = "2023-01-10"
#
# dates = get_date_range(start_date, end_date)
# print(dates)
