from django import template
from django.http import QueryDict
from django.utils.safestring import mark_safe
import urllib.parse

register = template.Library()


@register.simple_tag(takes_context=True)
def param_replace(context, **kwargs):
    """
    Return encoded URL parameters that are the same as the current
    request's parameters, only with the specified GET parameters added or changed.

    It also removes any empty parameters to keep things neat,
    so you can remove a parm by setting it to ``""``.

    For example, if you're on the page ``/things/?with_frosting=true&page=5``,
    then

    <a href="/things/?{% param_replace page=3 %}">Page 3</a>

    would expand to

    <a href="/things/?with_frosting=true&page=3">Page 3</a>

    Based on
    https://stackoverflow.com/questions/22734695/next-and-before-links-for-a-django-paginated-query/22735278#22735278
    """
    request = context["request"].GET 
    d = request.copy()
    list_all = d.lists()
    pre_dict = {}
    for k, v in list_all:
        pre_dict[k] = list(dict.fromkeys(v)).pop()
    for k, v in kwargs.items():
        pre_dict[k] = v    
    urlparams = urllib.parse.urlencode(pre_dict)
    return mark_safe(QueryDict(urlparams).urlencode())


@register.filter
def phone_number(number):
    """Convert a 10 character string into (xxx) xxx-xxxx."""
    if number:
        first = number[0:3]
        second = number[3:6]
        third = number[6:10]
        return '(' + first + ')' + ' ' + second + '-' + third