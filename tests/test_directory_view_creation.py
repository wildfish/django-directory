from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase
from directory.views import DirectoryView


class DirectoryViewCreation(TestCase):
    def test_no_filter_class_or_search_fields_are_present___improperly_configured_error_is_raised_when_the_directory_view_is_created(self):
        def _class_creation():
            class TestDirectoryView(DirectoryView):
                class Meta:
                    pass

        self.assertRaisesRegex(ImproperlyConfigured, 'Neither Meta.search_fields nor Meta.filter_class were set', _class_creation)

    def test_no_model_or_filter_class_are_set_but_search_fields_are_search_fields_are_present___improperly_configured_error_is_raised_when_the_directory_view_is_created(self):
        def _class_creation():
            class TestDirectoryView(DirectoryView):
                class Meta:
                    search_fields = ['field_a']

        self.assertRaisesRegex(ImproperlyConfigured, 'Neither Meta.filter_class nor Meta.model were set', _class_creation)

    def test_view_is_abstract___improperly_configured_error_is_raised_when_the_directory_view_is_constructed(self):
        def _class_creation():
            class TestDirectoryView(DirectoryView):
                class Meta:
                    abstract = True

            TestDirectoryView()

        self.assertRaisesRegex(ImproperlyConfigured, 'You cannot create and instance of an abstract DirectoryView', _class_creation)
