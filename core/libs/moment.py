'''
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# File: moment.py
# Project: core.wecare.id
# File Created: Tuesday, 27th November 2018 3:43:46 am
#
# Author: Arif Dzikrullah
#         ardzix@hotmail.com>
#         https://github.com/ardzix/>
#
# Last Modified: Tuesday, 27th November 2018 3:43:46 am
# Modified By: arifdzikrullah (ardzix@hotmail.com>)
#
# Handcrafted and Made with Love
# Copyright - 2018 Wecare.Id, wecare.id
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''


from datetime import datetime, timedelta
from django.utils.dateformat import format


def to_timestamp(dt):
    return format(dt, 'U')


def get_today_epoch():
    now = datetime.utcnow()
    return now.replace(now.year, now.month, now.day, 0, 0, 0, 0)


def get_difference_epoch(epoch):
    diff = datetime.utcnow() - epoch
    return int(diff.total_seconds() * 1000000)


def get_next_monday(today):
    today = today.date()
    return today + timedelta(days=-today.weekday(), weeks=1)


def get_last_monday(today, ):
    today = today.date()
    return today - timedelta(days=today.weekday(), )
