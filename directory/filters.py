from django_filters import FilterSet


def generate_model_filter_class(filter_model, filter_fields):
    class _Filter(FilterSet):
        class Meta:
            fields = filter_fields
            model = filter_model

    return _Filter
