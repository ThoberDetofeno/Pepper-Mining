"""
from peppermining import PepperMining
from filters.case_filter import CaseFilter
from kpi.number_of_events import NumberOfEvents


pm = PepperMining()
pm.read_event_log_csv("c:/Temp/base-peppermining/peppermining/tests/data/eventlog-example.csv", separator=';', format_date='%d/%m/%Y %H:%M')
pm.read_cases_csv("c:/Temp/base-peppermining/peppermining/tests/data/case-example.csv", separator=';')

f1 = CaseFilter(pm, [1, 5, 7, 8])
f1.get_event_log()
f2 = CaseFilter(f1, [3])
kp1 = NumberOfEvents(pm)
kp1.get_kpi()
pm.get_cases(['NumberOfEvents'])
"""
