from django import template

register = template.Library()


@register.filter
def render(obj, args):
    """
    Try to render an attribute from an object. It will first look for a function called 'render_<attr_name>',
    If this doesnt exist it will look for an attribute with the attribute name, if this doesnt exist it will
    fallback to the default value supplied or None if no default was supplied
    """
    splitargs = args.split(',')
    try:
        attribute, default = splitargs
    except ValueError:
        attribute, default = args, ''

    try:
        attr = obj.__getattribute__('render_' + attribute)
    except AttributeError:
        attr = obj.__dict__.get(attribute, None)

        if not attr:
            try:
                attr = obj.__getattribute__(attribute)
            except AttributeError:
                attr = obj.__dict__.get(attribute, default)

    if hasattr(attr, '__call__'):
        return attr.__call__()
    else:
        return attr


@register.filter
def get_selectable_pages(page, pages_before_after):
    # if we have few enough pages that we wouldn't have any breaks when we select the middle page give the full range
    # we also allow for the break occuring on the 2nd or penultimate pages
    if page.paginator.num_pages <= (5 + 2 * pages_before_after):
        return page.paginator.page_range

    # if the pages in the limit include the second pages starting at 1 otherwise have 1 and a break
    if page.number - pages_before_after <= 3:
        pages = [i for i in range(1, page.number)]
    else:
        pages = [1, None, ] + [i for i in range(page.number - pages_before_after, page.number)]

    # include the current page
    pages.append(page.number)

    # if the pages in the limit include the penultimate pages starting up to the final page are returned
    # otherwise have a break and then the final page
    if page.number + pages_before_after >= page.paginator.num_pages - 2:
        pages += [i for i in range(page.number + 1, page.paginator.num_pages + 1)]
    else:
        pages += [i for i in range(page.number + 1, page.number + pages_before_after + 1)] + [None, page.paginator.num_pages]

    return pages
