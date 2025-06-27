import datetime
import calendar

def handler(event, context): 
    return 'Hello from AWS Lambda using Python' +datetime.datetime.now() + '!'

