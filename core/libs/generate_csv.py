import csv
from datetime import datetime
from django.http import HttpResponse, StreamingHttpResponse


class Echo:
    def write(self, value):
        return value


def generate_csv(data, filename, headers, start_time=None, end_time=None):
    """
    data => List of list [[],[],[]]
    """
    if not start_time and not end_time:
        date = datetime.utcnow().strftime("%Y-%M-%d")
    else:
        date = '{}_{}'.format(start_time, end_time)

    echo_buffer = Echo()
    writer = csv.writer(echo_buffer)
    data = [headers] + data
    rows = (writer.writerow(_data) for _data in data)

    response = StreamingHttpResponse(rows, content_type='text/csv')
    filename = '{}_{}'.format(filename, date)
    response['Content-Disposition'] = 'attachment; filename="{}.csv"'.format(filename)
    return response