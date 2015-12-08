from django.template import Library
import datetime
from django.utils.timesince import timesince
register = Library()

# Returns a list containing range made from given value
# Usage (in template): {% for i in 3|get_range %}
@register.filter
def get_range( value ):
    return range( value )

@register.filter
def increment( i ):
    return i+1

# Usage (in template):
# {% for a,b in first_list|zip_lists:second_list %}
# {% endfor %}
@register.filter
def zip_lists(a, b):
    return zip(a, b)

@register.filter
def age(value):
    now = datetime.datetime.now(datetime.timezone.utc)
    try:
        difference = now - value
    except:
        return "Invalid input"
    if difference <= datetime.timedelta(minutes=1):
        return 'just now'
    return '%(time)s ago' % {'time': timesince(value).split(', ')[0]}
