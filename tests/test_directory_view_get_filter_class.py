from collections import OrderedDict
from django import forms
from django.test import TestCase
from directory.views import DirectoryView
from .models import TestModel, MultipleFieldModel


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

    def test_filter_class_is_not_set_and_form_class_is___result_is_generated_filter_class_with_the_correct_form(self):
        class FormClass(forms.Form):
            pass

        class TestDirectoryView(DirectoryView):
            class Meta:
                model = TestModel
                search_fields = ['field_a']
                form_class = FormClass

        v = TestDirectoryView()

        filter_class = v.get_filter_class()

        self.assertEqual(FormClass, filter_class.Meta.form)

    def test_filter_class_is_not_set_and_form_class_is_not_set___result_is_generated_filter_class_with_the_base_form(self):
        class TestDirectoryView(DirectoryView):
            class Meta:
                model = TestModel
                search_fields = ['field_a']

        v = TestDirectoryView()

        filter_class = v.get_filter_class()

        self.assertEqual(forms.Form, filter_class.Meta.form)

    def test_search_fields_are_specified_with_a_field___the_resulting_form_has_the_correct_field_objects_after_construction(self):
        second_field = forms.IntegerField(label='Second Field')
        min_field = forms.IntegerField(label='Min')
        max_field = forms.IntegerField(label='Max')

        class TestDirectoryView(DirectoryView):
            class Meta:
                model = MultipleFieldModel
                search_fields = OrderedDict((
                    ('first', ['exact']),
                    ('second', [
                        ('exact', second_field)
                    ]),
                    ('third', [
                        ('gte', min_field),
                        ('lte', max_field),
                    ])
                ))

        v = TestDirectoryView()

        filter_class = v.get_filter_class()
        form = filter_class.Meta.form()

        self.assertEqual(second_field, form.fields['second__exact'])
        self.assertEqual(min_field, form.fields['third__gte'])
        self.assertEqual(max_field, form.fields['third__lte'])

    def test_search_fields_are_specified_with_a_field___the_resulting_filter_has_the_correct_fields_set(self):
        second_field = forms.IntegerField(label='Second Field')
        min_field = forms.IntegerField(label='Min')
        max_field = forms.IntegerField(label='Max')

        class TestDirectoryView(DirectoryView):
            class Meta:
                model = MultipleFieldModel
                search_fields = OrderedDict((
                    ('first', ['exact']),
                    ('second', [
                        ('exact', second_field)
                    ]),
                    ('third', [
                        ('gte', min_field),
                        ('lte', max_field),
                    ])
                ))

        v = TestDirectoryView()

        filter_class = v.get_filter_class()

        expected_fields = OrderedDict((
            ('first', ['exact']),
            ('second', ['exact']),
            ('third', ['gte', 'lte']),
        ))

        self.assertEqual(expected_fields, filter_class.Meta.fields)
