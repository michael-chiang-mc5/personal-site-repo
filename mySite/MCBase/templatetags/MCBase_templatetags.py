from django.template import Library
register = Library()

# Returns a list containing range made from given value
# Usage (in template): {% for i in 3|get_range %}
@register.filter
def get_range( value ):
  return range( value )

@register.filter
def increment( i ):
  return i+1
