import math
from datetime import date, datetime
from dateutil import parser
import plotly
plotly.tools.set_credentials_file(username='pmoolrajani', api_key='lqy9gutcnu')
import plotly.plotly as py
from plotly.graph_objs import *

# setting constants
__EVENT_TYPES = {
    'incidents':{'risk': 0.5, 'sla':3},
    'patching':{'risk': 0.3, 'sla': 7},
    'misc':{'risk': 0.2, 'sla': 5}
}
__SCORE_MAX = 1000
__SCORE_MIN = 0
__NO_EVENTS_FRACTION = 0.90
__TIME_INTERVAL = 7
__NUM_DAYS = 30


# setting initial values
score_avg_company = 620
score_emp = score_avg_company
risk = 0.5

#dict_score = {'2016-08-01':{'score':'', events:[]}}
#dict_events = {'<event_id>':{'event_date':'', 'event_type':'', 'event_res_date':''}

    
# creating dictionary of events from the input csv file
dict_events = {}
file_events = open('pmoolrajani-002.csv').readlines()

   
dict_events = {}
for line in file_events:
    
    event_details = line.split(',')
    if event_details[0] != 'event_date':
        event_date = parser.parse(event_details[0].strip())
        event_type = event_details[1].strip()
        num_events_recv = event_details[2].strip()
        num_events_resp = event_details[3].strip()
        num_events_sla_breach = event_details[4].strip()

        dict_events[event_date] = {}
        dict_events[event_date]['event_type'] = event_type
        dict_events[event_date]['num_events_recv'] = num_events_recv
        dict_events[event_date]['num_events_resp'] = num_events_resp
        dict_events[event_date]['num_events_sla_breach'] = num_events_sla_breach
        
        print (dict_events[event_date])


for i in range(1, __NUM_DAYS+1, __TIME_INTERVAL):
    
    # calculating confidence intervals for employee score
    cpos = math.sqrt(__SCORE_MAX - score_emp)
    cneg = math.sqrt(score_emp)

    # calculating upper and lower limit of security score of an employee for __TIME_INTERVAL
    score_cpos = score_emp + cpos
    score_cneg = score_emp - cneg
    
    no_events_counter = 0
    for j in range(i,i+__TIME_INTERVAL):
        if j > 31:
            break
        date_counter = datetime(2016, 8, j, 0, 0)
        
        if num_events_recv == 0:
            no_events_counter += 1
            
        for range in (0, dict_events[date_counter]['num_events_resp']):
            score_emp = score_emp + (score_cpos - score_emp)*(risk)
        for range in (0, dict_events[date_counter]['num_events_sla_breach']):
            score_emp = score_emp - (score_emp - score_cneg)*(risk)
        
    if no_events_counter == __TIME_INTERVAL:
        score_emp = score_cpos
        
    print (score_emp)  
#score_emp = score_emp - (score_emp - score_cneg)*(risk)
#score_emp = score_emp + (score_cpos - score_emp)*(risk)
