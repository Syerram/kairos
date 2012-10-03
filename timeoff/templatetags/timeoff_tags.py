'''
Created on Sep 15, 2012

@author: staticfish
'''
from django import template
from workflow.models import ApproverQueue

register = template.Library()

def is_approved(booked_timeoff):
    return booked_timeoff.last_status == ApproverQueue.approved_status()

register.filter("is_approved", is_approved)
