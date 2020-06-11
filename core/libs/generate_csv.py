import csv
from datetime import datetime
from django.http import HttpResponse, StreamingHttpResponse


def generate_csv(data, filename, headers, start_time=None, end_time=None):
    """
    data => List of list [[],[],[]]
    """
    if not start_time and not end_time:
        date = datetime.utcnow().strftime("%Y-%M-%d")
    else:
        date = '{}_{}'.format(start_time, end_time)

    response = StreamingHttpResponse(content_type='text/csv')
    filename = '{}_{}'.format(filename, date)
    response['Content-Disposition'] = 'attachment; filename="{}.csv"'.format(filename)
    writer = csv.writer(response)
    writer.writerow(headers)
    for _data in data:
        writer.writerow(_data)
    return response