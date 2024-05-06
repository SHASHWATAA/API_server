import json
from datetime import datetime, date, timedelta
from invoice_generator import timesheet_json


def get_worked_data(json_data, _required_dates):
    """
    :rtype: dict
    """
    d = json.loads(json_data, strict=False)
    worked_data = {'data': []}

    for required_date in _required_dates:
        # required dates are the days of the week we and the output is in the format to %Y-%m-%d.
        # datetime.fromisoformat(x['Date']).strftime('%Y-%m-%d') is the current date in the API formatted to %Y-%m-%d
        # need to do this because api displays more than what we need.

        var = [x for x in d if datetime.fromisoformat(x['Date']).strftime('%Y-%m-%d') == required_date]

        if len(var) == 0:
            invoice_date = datetime.fromisoformat(required_date).strftime('%Y/%m/%d')
            day = datetime.fromisoformat(required_date).strftime('%A')
            net_worked_seconds = 0
            time_in = ""
            break_start = ""
            break_end = ""
            time_out = ""
            total_hours = "00:00"

            worked_datum = make_invoice_json_data(invoice_date, day, time_in, break_start, break_end, time_out,
                                                  total_hours, net_worked_seconds)
            worked_data['data'].append(worked_datum)

        else:
            start = datetime.fromisoformat(var[0]['StartTimeLocalized'])
            end = datetime.fromisoformat(var[0]['EndTimeLocalized'])

            worked_seconds = (end - start).seconds
            try:
                break_seconds = var[0]['Slots'][0]['intEnd'] - var[0]['Slots'][0]['intStart']
            except IndexError:
                break_seconds = 0

            net_worked_seconds = worked_seconds - break_seconds
            worked_h_m_s = str(timedelta(seconds=net_worked_seconds))
            y = worked_h_m_s.split(":")
            worked_h_m = f"{y[0]}:{y[1]}"

            invoice_date = datetime.fromisoformat(var[0]['Date']).strftime('%Y/%m/%d')
            day = datetime.fromisoformat(var[0]['Date']).strftime('%A')
            time_in = start.strftime('%I:%M')

            if break_seconds == 0:
                break_start = "-"
                break_end = "-"
            else:
                break_start = "12:30"
                break_end = "1:00"

            time_out = end.strftime('%I:%M')
            total_hours = worked_h_m

            worked_datum = make_invoice_json_data(invoice_date, day, time_in, break_start, break_end, time_out,
                                                  total_hours, net_worked_seconds)

            worked_data['data'].append(worked_datum)

            # print(x['Date'], net_worked_seconds / 3600, worked_h_m)

    return worked_data


def get_week_dates(week):
    if week == 0:
        today = date.today()
    else:
        today = date.today() - timedelta(days=7)

    weekday = today.isoweekday()
    # The start of the week
    start = today - timedelta(days=weekday - 1)
    # build a simple range
    dates = [start + timedelta(days=d) for d in range(7)]
    dates = [str(d) for d in dates]

    return dates


def make_invoice_json_data(invoice_date, day, time_in, break_start, break_end, time_out, total_hours, worked_seconds):
    return {'Date': invoice_date, 'Day': day, "Time In": time_in, "Break Start": break_start, "Break End": break_end,
            "Time Out": time_out, "Total Hours": total_hours, "worked_seconds": worked_seconds}


if __name__ == '__main__':
    data = timesheet_json.using_selenium()
