'''
Created on Sep 16, 2012

@author: staticfish
'''
from django import forms
from timeoff.models import BookTimeOff, BookTimeOfffHistory
from workflow.models import ApproverQueue

class BookTimeOffForm(forms.ModelForm):
    
    class Meta:
        model = BookTimeOff
        
    def __init__(self, *args, **kwargs):
        super(BookTimeOffForm, self).__init__(*args, **kwargs)
    
    def is_valid(self):
        """
        #TODO:
        1. dates are in future
        2. validations for dates
            2.1 time remaining + overdraw_limit - time-approved in future - time-unapproved to (end - start) 
            2.2 if under, raise exception. This shouldn't have happened since JS should have taken care of it
            2.3 if over, then add to the BookTimeOff
        """  
        return super(BookTimeOffForm, self).is_valid()

    def save(self, commit=True):
        book_timeoff = super(BookTimeOffForm, self).save(commit)
        status = ApproverQueue.in_queue_status()
        
        booktimeoff_inqueue_history = BookTimeOfffHistory(book_timeoff=book_timeoff, book_timeoff_status=status)
        booktimeoff_inqueue_history.save()
        
        return book_timeoff
