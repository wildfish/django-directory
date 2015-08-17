from django.test import TestCase
from directory.views import DirectoryView
from .models import TestModel


class DirectoryViewGetFilterClass(TestCase):
    def test_filter_class_is_set_but_search_fields_are_not___result_is_filter_class(self):
        class FilterClass(object):
            class Meta:
                model = TestModel

        class TestDirectoryView(DirectoryView):
            class Meta:
                filter_class = FilterClass

        v = TestDirectoryView()

        self.assertEqual(FilterClass, v.get_filter_class())

    def test_filter_class_and_search_fields_are_set___result_is_filter_class(self):
        class FilterClass(object):
            class Meta:
                model = TestModel

        class TestDirectoryView(DirectoryView):
            class Meta:
                filter_class = FilterClass
                search_fields = ['field_a']

        v = TestDirectoryView()

        self.assertEqual(FilterClass, v.get_filter_class())

    def test_filter_class_is_not_set_and_search_fields_are_set___result_is_filter_class_generated_from_the_model_and_fields(self):
        class TestDirectoryView(DirectoryView):
            class Meta:
                model = TestModel
                search_fields = ['field_a']

        v = TestDirectoryView()

        filter_class = v.get_filter_class()

        self.assertEqual(TestModel, filter_class.Meta.model)
        self.assertEqual(['field_a'], filter_class.Meta.fields)
