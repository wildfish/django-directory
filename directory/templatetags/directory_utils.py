from django import template

register = template.Library()


@register.filter
def getattr(obj, args):
    """ Try to get an attribute from an object.

    Example: {% if block|getattr:"editable,True" %}

    Beware that the default is always a string, if you want this
    to return False, pass an empty second argument:
    {% if block|getattr:"editable," %}
    """
    splitargs = args.split(',')
    try:
        attribute, default = splitargs
    except ValueError:
        attribute, default = args, ''

    try:
        attr = obj.__getattribute__(attribute)
    except AttributeError:
        attr = obj.__dict__.get(attribute, default)

    if hasattr(attr, '__call__'):
        return attr.__call__()
    else:
        return attr
