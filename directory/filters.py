from collections import OrderedDict
from django import forms
from django_filters import FilterSet
import six


def generate_form_class(filter_fields):
    """
    Creates a custom form class that respects the new fields if they have been set in the filter_fields
    """
    # If we are just dealing with a list of fields we can let django-filter handle the form creation
    if not isinstance(filter_fields, dict):
        return forms.Form

    # We need to store the field names and the new field values for all fields that a new value has been set
    modified_fields = {}
    for field_name, lookups in filter_fields.items():
        for lookup in lookups:
            if isinstance(lookup, six.string_types):
                continue

            modified_fields[field_name + '__' + lookup[0]] = lookup[1]

    # Create the form class that will swap out any moodified fields on construction
    class _Form(forms.Form):
        def __init__(self, *args, **kwargs):
            super(_Form, self).__init__(*args, **kwargs)

            for name, new_field in modified_fields.items():
                self.fields[name] = new_field

    return _Form


def _extract_simplified_filter_fields(filter_fields):
    """
    Takes the filter_fields and simplifies them to a form django-filter can understand
    """
    # If we are just dealing with a list we are fine
    if not isinstance(filter_fields, dict):
        return filter_fields

    # if we are dealing with a dictionary we need to take all the fields and only store the lookups
    # (not the modified fields)
    _filter_fields = OrderedDict()

    for field_name, lookups in filter_fields.items():
        _filter_fields[field_name] = []
        for lookup in lookups:
            if isinstance(lookup, six.string_types):
                # if the lookup is a string then we are fine
                _filter_fields[field_name].append(lookup)
            else:
                # if the lookup is a tuple we need to only store the lookup string from it
                _filter_fields[field_name].append(lookup[0])

    return _filter_fields


def generate_model_filter_class(filter_model, filter_fields, form_class):
    if form_class is None:
        form_class = generate_form_class(filter_fields)

    class _Filter(FilterSet):
        class Meta:
            fields = _extract_simplified_filter_fields(filter_fields)
            model = filter_model
            form = form_class

    return _Filter
