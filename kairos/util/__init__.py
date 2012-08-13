"""Contains utility packages"""
from django.contrib.messages.storage.session import SessionStorage
from django.conf import settings
from datetime import date, datetime, timedelta, time as time_obj


class ExternalMessageRequestStorage(SessionStorage):
    #TODO
    def __init__(self, request, *args, **kwargs):
        super(ExternalMessageRequestStorage, self).__init__(request, *args, **kwargs)
    
    def add(self, level, message, extra_tags=''):
        '''
        prepares the message. uses external file to load the messages
        '''
        KAIROS_MESSAGE_SETTING = u"SINDEO_MESSAGES"
        if message.startswith('sindeo.message'):
            sindeo_messages = getattr(settings, KAIROS_MESSAGE_SETTING, {})
            if message in sindeo_messages:
                message = sindeo_messages[message]
            else:
                message = '{no message found. message 1001}'
        super(ExternalMessageRequestStorage, self).add(level, message, extra_tags)
        
def determine_period(the_date=date.today()):
    """determines the start and end date of the week and returns tuple"""
    start_week = date.today() - timedelta(days=date.today().weekday())
    end_week = start_week + timedelta(days=6)
    
    return (start_week, end_week,)
    
    
    
    
