import csv
from datetime import datetime
from io import StringIO
from django.http import HttpResponse, StreamingHttpResponse


def generate_csv(
        data, filename, headers,
        send_email=False, start_time=None, end_time=None):
    """
    data => List of list [[],[],[]]
    """
    if not start_time and not end_time:
        date = datetime.utcnow().strftime("%Y-%m-%d")
    else:
        date = '{}_{}'.format(start_time, end_time)

    content_type = "text/csv"
    csvfile = StringIO()
    csvwriter = csv.writer(csvfile)

    data = [headers] + data
    for _data in data:
        csvwriter.writerow(_data)

    filename = '{}_{}.csv'.format(filename, date)
    data = csvfile.getvalue()

    return filename, data, content_type

    # response = HttpResponse(data, content_type=content_type)
    # response['Content-Disposition'] = 'attachment; filename="{}"'.format(
    #     filename)
    # return response
