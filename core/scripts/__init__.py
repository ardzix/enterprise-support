'''
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# File: __init__.py
# Project: core.bimaasia.id
# File Created: Tuesday, 18th June 2019 3:24:59 pm
# 
# Author: Arif Dzikrullah
#         ardzix@hotmail.com>
#         https://github.com/ardzix/>
# 
# Last Modified: Tuesday, 18th June 2019 3:25:00 pm
# Modified By: arifdzikrullah (ardzix@hotmail.com>)
# 
# Handcrafted and Made with Love - Ardz
# Copyright - 2019 PT Bima Kapital Asia Teknologi, bimaasia.id
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''

from core.scripts.administrative import *
from core.scripts.branch import *
from core.scripts.agreement import *
from core.scripts.numbering import *

def generate_master_data():
    import_provices()
    import_regencies()
    import_branches()