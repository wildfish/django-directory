django-directory
================

django-directory is an app that allows for easy creation of a searchable directory of objects.

Usage
=====

The minimum requirement for creating a searchable directory with django-directory is to create a view which inherits
from the `DirectoryView` and specifies the model to create the view for:

```
from directory.view import DirectoryView


class MyView(DirectoryView):
    class Meta:
        model = MyModel
```

This will produce a table with all fields visible which is also filterable by all fields. The fields to filter on and 
display can also be specified in the `Meta` class:

```
from directory.view import DirectoryView


class MyView(DirectoryView):
    class Meta:
        model = MyModel
        search_fields = ['name', 'age']
        display_fields = ['name', 'age', 'property_1', 'property_2']
```

This will create a table with only the 'name', 'age', 'property_1' and 'property_2' fields present which is filterable
by 'name' and 'age'.

By default the heading to use for each column is the title case if the verbose name of the field, this can be 
overridden however by passing a `tuple` of `(field_name, override_name)`, for example, if we had
`display_fields = [('name', 'Full Name'), 'age']` the heading of the 'name' column would be 'Full Name' and the 'age' 
column would use the `verbose_name` of the field.
 
Behind the scenes django-filter is used to handle the queryset filtering. This allows for fields to use all the 
selectors available in django-filter, for example:

```
search_fields = OrderDict(
    ('name', ['icontains']),
    ('age', ['gte', 'lte']),
)
```

This would give a filter which performs a case insensitive search of the name field and a search of all people within
the age range supplied. For a full description of valid field specification see: 
[http://django-filter.readthedocs.org/en/latest/usage.html#the-filter](http://django-filter.readthedocs.org/en/latest/usage.html#the-filter)

**NOTE:** We recommend using a ordered dictionary for `search_fields` otherwise the ordering of your form may change.

Modifying The Form
==================

Using the Meta class
--------------------

You can modify the behaviour of the form by supplying the Meta class with the `form_class` property. This allows you to
modify the form on construction. For example if we had a form with an upper and lower rating we would specify our view
as:

```
class RatingSearchView(DirectoryView):
    class Meta:
        search_fields = OrderedDict(
            ('rating', ['gte', 'lte']),
        )
```

This would give two fields labeled 'Rating' however which would not be too useful. If we do the following:

```
class RatingSearchForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(RatingSearchForm, self).__init__(*args, **kwargs)
        
        self.fields['rating__gte'].label = _('Minimum rating')
        self.fields['rating__lte'].label = _('Maximum rating')
        

class RatingSearchView(DirectoryView):
    class Meta:
        search_fields = OrderedDict(
            ('rating', ['gte', 'lte']),
        )
        form_class = RatingSearchForm
```

We would end up with two fields, one labeled 'Minimum rating' and the other labeled 'Maximum Rating'.

Setting Field Objects
---------------------

You can also specify field objects in the search fields, to do this we replace the lookups with a tuple of lookup name
and field object. To acieve the same as above we could do:

```
class RatingSearchView(DirectoryView):
    class Meta:
        search_fields = OrderedDict(
            ('rating', [
                ('gte', forms.IntegerField(label=_('Minimum rating')))
                ('lte', forms.IntegerField(label=_('Maximum rating')))
            ]),
        )
        form_class = RatingSearchForm
```

Template
========

The default template used is `directory/base.html` and assumes you have a base template for your site called `base.html`
which has a main block called `content`. To override this behaviour set the `template_name` on the view class.

The following values are set in the template context in addition to the usual values sent by the `ListView`:

**display_headings:** Flag whether to show the heading row or not.

**field_headings:** The headings to display for each field (in display order).

**field_names:** The names of the fields to display (in display order).

**filter:** The filter object, use `filter.form` to access the search form.

**filter_query_string:** The query string supplied by the filter.

**link_on_field:** The name of the field to add the link to.

Meta Fields
===========

**abstract:** Used to create an abstract base class (useful when you do not want to specify `search_fields` or 
`filter_class`)

**display_fields:** The fields to display and optionally the name to use as the heading. This should be a list of field
names or tuples of field names and the heading name. Example: `display_fields = [('name', 'Full Name'), 'age']`

**display_headings:** Flag to show the heading row or not.

**filter_class:** Used if you don't want to use the filter generated by django-directory. See 
[http://django-filter.readthedocs.org/en/latest/usage.html#the-filter](http://django-filter.readthedocs.org/en/latest/usage.html#the-filter)

**form_class:** Used to override the default behaviour of the search form.

**link_on_field:** The name of the field to add the details link to, this link is taken from `get_absolute_url` on the 
model. If this is not set the first field is chosen. To have no link use None. 

**model:** The model to create the directory for.

**search_fields:** The fields to use in the search form, this can be a list of fields in which case the filter will 
search for exact matches or a dictionary of fields to lookups. Example:
 
```
search_fields = OrderDict(
    ('name', ['icontains']),
    ('age', ['gte', 'lte']),
)
```
