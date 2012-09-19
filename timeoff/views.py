# Create your views here.
from configuration.models import UserTimeOffPolicy
from django.contrib.auth.decorators import login_required
from timeoff.models import BookTimeOff
from datetime import date, timedelta
from django.utils import simplejson
from django.http import HttpResponse
from kairos.util import DecimalEncoder, render_to_html_dict

@login_required
def timeoff_left(request, timeoff):
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
    #fetch unapproved time and approved but in future    
    future_date = date.today() + timedelta(days=1)    
    bookings = BookTimeOff.objects.bookings_sofar(request.user, after_date=future_date)
    booked_days = 0;
    for booking in bookings:
        delta = booking.end_date - booking.start_date
        booked_days += delta.days
        
    data = simplejson.dumps({'time_remaining':time_remaining, 'overdraw_limit': overdraw_limit, 'booked_days': booked_days}, cls=DecimalEncoder, ensure_ascii=False)
    return HttpResponse(data, mimetype='application/json')
        
@login_required
@render_to_html_dict(
                     {'timeoff-main':'timeoff/main.html',
                      'book-timeoff': 'timeoff/book_timeoff.html'
                    })
def timeoff_book(request):
    """
        Books timeoff for the individual. It creates a entry in BookTimeOff and starts the Queue for approval.
        It wont deduct time-remaining till the individual has taken the time off and entered the time-off taken in the timesheet.        
        
        Coding Notes:
        1. Create BookTimeOffForm and give it all the POST details
        2. add validations to Form for
            2.1 time remaining + overdraw_limit - time-approved in future - time-unapproved to (end - start) 
            2.2 if under, raise exception. This shouldn't have happened since JS should have taken care of it
            2.3 if over, then add to the BookTimeOff
    
        Create ApprovalQueue process, by sending it a signal
    """
    if request.method == 'GET':
        return 'book-timeoff', {}
    else:
        print request.POST
        return 'book-timeoff', {}