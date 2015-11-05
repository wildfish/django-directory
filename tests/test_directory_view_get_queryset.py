from django.test import TestCase, RequestFactory
from django_filters import FilterSet
from directory.views import DirectoryView
from .models import TestModel


class DirectoryViewGetQueryset(TestCase):
    def test_result_is_unfiltered_queryset_filtered_by_the_filter_class(self):
        class FilterClass(FilterSet):
            class Meta:
                model = TestModel

            @property
            def qs(self):
                return {
                    'filter_data': self.data,
                    'unfiltered_qs': self.queryset,
                }

        class TestDirectoryView(DirectoryView):
            class Meta:
                filter_class = FilterClass

            def get_unfiltered_queryset(self):
                return 'unfiltered qs'

        request = RequestFactory().get('/?field_a=1')
        v = TestDirectoryView()
        v.request = request
        qs = v.get_queryset()

        self.assertEqual({
            'filter_data': request.GET,
            'unfiltered_qs': v.get_unfiltered_queryset(),
        }, qs)
