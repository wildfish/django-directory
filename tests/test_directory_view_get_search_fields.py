from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase

from directory.views import DirectoryView
from .models import TestModel


class DirectoryViewGetSearchFields(TestCase):
    def test_search_fields_are_not_specified___improperly_configured_error_is_raised(self):
        class TestDirectoryView(DirectoryView):
            unfiltered_queryset = TestModel.objects.all()
            
            class Meta:
                model = TestModel

        self.assertRaisesRegex(ImproperlyConfigured, 'Neither Meta.search_fields nor Meta.filter_class were set', TestDirectoryView().get_search_fields)

    def test_search_fields_are_specified___search_fields_are_returned(self):
        class TestDirectoryView(DirectoryView):
            class Meta:
                model = TestModel
                search_fields = ['field_a']

        self.assertEqual(['field_a'], TestDirectoryView().get_search_fields())
