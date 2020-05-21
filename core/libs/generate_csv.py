import csv
from datetime import datetime
from django.http import HttpResponse


def generate_csv(data, filename, headers, start_time, end_time):
    """
    data => List of list [[],[],[]]
    """
    response = HttpResponse(content_type='text/csv')
    filename = f'{filename}_{start_time}_{end_time}'
    response['Content-Disposition'] = f'attachment; filename="{filename}.csv"'
    writer = csv.writer(response)
    writer.writerow(headers)
    for _data in data:
        writer.writerow(_data)
    return response