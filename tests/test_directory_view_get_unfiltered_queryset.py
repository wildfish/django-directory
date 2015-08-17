from django.test import TestCase
from django_filters import FilterSet
from directory.views import DirectoryView
from .models import TestModel, TestModelB


class DirectoryViewGetUnfilteredQueryset(TestCase):
    def test_unfiltered_query_set_is_set___result_is_the_set_queryset(self):
        class FilterClass(FilterSet):
            class Meta:
                model = TestModel

        class TestDirectoryView(DirectoryView):
            unfiltered_queryset = 'some set'
            
            class Meta:
                filter_class = FilterClass

        v = TestDirectoryView()
        qs = v.get_unfiltered_queryset()

        self.assertEqual('some set', qs)

    def test_filter_class_is_set_model_is_not___result_is_all_objects_from_filter_model(self):
        class FilterClass(FilterSet):
            class Meta:
                model = TestModel

        class TestDirectoryView(DirectoryView):
            class Meta:
                filter_class = FilterClass

        v = TestDirectoryView()
        qs = v.get_unfiltered_queryset()

        self.assertEqual(str(TestModel.objects.all().query), str(qs.query))

    def test_filter_class_and_model_is_are_set___result_is_all_objects_from_filter_model(self):
        class FilterClass(FilterSet):
            class Meta:
                model = TestModel

        class TestDirectoryView(DirectoryView):
            class Meta:
                filter_class = FilterClass
                model = TestModelB

        v = TestDirectoryView()
        qs = v.get_unfiltered_queryset()

        self.assertEqual(str(TestModel.objects.all().query), str(qs.query))

    def test_model_is_set_filter_class_is_not___result_is_all_objects_from_model(self):
        class TestDirectoryView(DirectoryView):
            class Meta:
                model = TestModelB
                search_fields = ['field_b']

        v = TestDirectoryView()
        qs = v.get_unfiltered_queryset()

        self.assertEqual(str(TestModelB.objects.all().query), str(qs.query))
