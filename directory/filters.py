from django_filters import FilterSet


def generate_model_filter_class(filter_model, filter_fields, form_class):
    class _Filter(FilterSet):
        class Meta:
            fields = filter_fields
            model = filter_model
            form = form_class

    return _Filter
