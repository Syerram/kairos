# Create your views here.
from configuration.models import UserTimeOffPolicy
from datetime import date, timedelta
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils import simplejson
from kairos.util import DecimalEncoder, render_to_html_dict, cacher
from timeoff.forms import BookTimeOffForm
from timeoff.models import BookTimeOff, BookTimeOfffHistory
import workflow
from rules.models import RuleSet
from rules.validators import GenericAspect
from common.models import DropdownValue
import datetime
import calendar

#TODO: cache user/timeoff combination

@login_required
def timeoff_left(request, timeoff, start_date=None):
    """
        Returns time remaining for the logged in user. 
        It returns, the 
            time remaining : derived directly from UserTimeOffPolicy
            overdraw_limit: derived directly from UserTimeOffPolicy
            time_booked: sum of booked time that are un-approved and approved time that are in future
            
            The time remaining is sum of 'time_remaining + overdraw_limit - time_booked_unapproved - time_booked_approved_future    
    """
    #fetch policies for the given TimeOff. We should technically have only one TimeOff. 
    policies = UserTimeOffPolicy.objects.policies(request.user, timeoff)
    time_remaining, overdraw_limit = (0, 0)
    for policy in policies:
        time_remaining += policy.time_remaining
        overdraw_limit += policy.max_overdraw_limit
        
    #TODO: perhaps use raw SQL to get the total time instead of so many SQLs
    #fetch unapproved time and approved for the given month
    if not start_date:
        start_date = datetime.date(date.today().year, date.today().month, 1)
    
    #Bookings so far should return bookings starting from start date and any in the future
    #The assumption is that the timeoffs in the past would have been already approved and logged
    '''
    TODO: for those like me, this is a bug because without logging time, I can actually take more timeoff since I haven't logged my time yet
    which would mean that, it will always show more timeoff available then it should be.
    Perhaps we should just deduct on approval that way we wont end up with that bug.
    We would then need to show super/HR that individual took timeoff for timeoffs that require booking and that didn't match to any approved timeoff bookings    
    '''
    bookings = BookTimeOff.objects.bookings_sofar(request.user, start_date=start_date, timeoff_type=timeoff)
    booked_days = 0;
    for booking in bookings:
        #exclude approved ones, since they are already deducted from the time_remaining
        if booking.last_status.book_timeoff_status <> DropdownValue.objects.dropdownvalue('WF', 'APPRD'):
            delta = booking.end_date - booking.start_date
            booked_days += (delta.days + 1) #inclusive of start date
        
    data = simplejson.dumps({'time_remaining':time_remaining, 'overdraw_limit': overdraw_limit, 'booked_days': booked_days}, cls=DecimalEncoder, ensure_ascii=False)
    return HttpResponse(data, mimetype='application/json')
        
@login_required
@render_to_html_dict(
                     {'timeoff-main':'timeoff/main.html',
                      'book-timeoff': 'timeoff/book_timeoff.html'
                    })
def timeoff_book(request, start_date=None):
    """
        Books timeoff for the individual. It creates a entry in BookTimeOff and starts the Queue for approval.
        It wont deduct time-remaining till the individual has taken the time off and entered the time-off taken in the timesheet.        
        
        Coding Notes:
        1. Create BookTimeOffForm and give it all the POST details
        2. validate BookTimeOffForm [see BookTimeOffForm.is_valid() method]
    
        Create ApprovalQueue process, by sending it a signal
    """
    if request.method == 'GET':
        return 'book-timeoff', timeoff_bookings(request, start_date)
    else:
        booktimeoff_form = BookTimeOffForm(request.POST)
        if booktimeoff_form.is_valid():
            booktimeoff = booktimeoff_form.save()
            workflow.signals.post_attach_queue_save_event.send(sender=BookTimeOff, instance=booktimeoff, is_draft=False)

            #check if we have validators 
            #TODO: have all forms extend RuleEnabledForm that on save can actually run the ruleSet.            
            rule_set = RuleSet.objects.for_instance(booktimeoff)
            if rule_set:
                errors = GenericAspect.validate(rule_set, booktimeoff)
                if errors:
                    raise TypeError('ruleset errors encountered')
            
        #TODO: circulate back to main html
        return 'book-timeoff', {}

@login_required
def timeoff_bookings(request, start_date=None):
    bookings_data = {'REJTD': [], 'APPRD': [], 'INPROC': []}
    
    #TODO: Consolidate
    if not start_date:
        start_date = datetime.date(date.today().year, date.today().month, 1)
    else:
        start_date = datetime.datetime.strptime(start_date, '%Y%m%d')        
    
    bookings = BookTimeOff.objects.bookings_sofar(request.user, start_date=start_date)
    for booking in bookings:
        booking_data = {}
        booking_data['title'] = booking.title if booking.title else booking.timeoff_type.name
        booking_data['start'] = booking.start_date.strftime('%Y-%m-%d')
        booking_data['end'] = booking.end_date.strftime('%Y-%m-%d')
        if booking.last_status.book_timeoff_status == DropdownValue.objects.dropdownvalue('WF', 'APPRD'):
            bookings_data['APPRD'].append(booking_data)
        elif booking.last_status == DropdownValue.objects.dropdownvalue('WF', 'REJTD'):
            bookings_data['REJTD'].append(booking_data)
        else:
            bookings_data['INPROC'].append(booking_data)            
    if request.is_ajax():
        data = simplejson.dumps(bookings_data, cls=DecimalEncoder, ensure_ascii=False)
        return HttpResponse(data, mimetype='application/json')
    else:
        return {'bookings': bookings_data}

def post_final_status_update(sender, **kwargs):
    """
        Post the final status to be updated
        Called by signal
    """
    book_timeoff = kwargs['instance']
    booktimeoff_inqueue_history = BookTimeOfffHistory(book_timeoff=book_timeoff, book_timeoff_status=kwargs['status'])
    booktimeoff_inqueue_history.save()
    #decrement time-remaining
    
    policies = UserTimeOffPolicy.objects.policies(book_timeoff.user, book_timeoff.timeoff_type.id)
    for policy in policies:
        policy.time_remaining -= book_timeoff.number_of_days
        #overdrawn, attempt to remove from overdraw property. if overdraw becomes negative, throw exception
        if policy.time_remaining < 0:
            policy.max_overdraw_limit += policy.time_remaining
            policy.time_remaining = 0
            
        policy.save()
