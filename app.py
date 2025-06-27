import datetime
import calendar

time = datetime.datetime.now()
str_time = time.strftime('%Y/%m/%d %H:%M:%S')

def handler(event, context): 
    return 'Hello from AWS Lambda using Python' + str_time  + '!'

