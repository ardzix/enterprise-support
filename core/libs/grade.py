'''
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# File: grade.py
# Project: kur.bri.co.id
# File Created: Saturday, 23rd May 2020 12:56:46 pm
#
# Author: Arif Dzikrullah
#         ardzix@hotmail.com>
#         https://github.com/ardzix/>
#
# Last Modified: Saturday, 23rd May 2020 12:56:46 pm
# Modified By: Arif Dzikrullah (ardzix@hotmail.com>)
#
# Handcrafted and Made with Love - Ardz
# Copyright - 2020 PT Bank Rakyat Indonesia, bri.co.id
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''


def get_score_range_from_grade(grade):
    if grade == 10:
        start = 396
        end = 597
    elif grade == 9:
        start = 598
        end = 626
    elif grade == 8:
        start = 627
        end = 644
    elif grade == 7:
        start = 645
        end = 657
    elif grade == 6:
        start = 658
        end = 669
    elif grade == 5:
        start = 670
        end = 680
    elif grade == 4:
        start = 681
        end = 691
    elif grade == 3:
        start = 692
        end = 703
    elif grade == 2:
        start = 704
        end = 721
    elif grade == 1:
        start = 722
        end = 825
    else:
        start = None
        end = None
    return (start, end)