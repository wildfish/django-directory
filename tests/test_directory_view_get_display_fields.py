from django.test import TestCase
from directory.views import DirectoryView
from .models import MultipleFieldModel


class DirectoryViewGetDisplayFields(TestCase):
    def test_no_fields_have_name_overrides___title_case_verbose_names_are_used_for_all_displayed_fields(self):
        class TestDirectoryView(DirectoryView):
            class Meta:
                model = MultipleFieldModel
                search_fields = ['first']
                display_fields = ['first', 'third']

        v = TestDirectoryView()
        fields = v.get_display_fields()

        self.assertEqual([
            ('first', 'First Field'),
            ('third', 'Third'),
        ], fields)

    def test_some_fields_have_name_overrides___title_case_verbose_names_are_used_for_all_displayed_fields_without_overrides(self):
        class TestDirectoryView(DirectoryView):
            class Meta:
                model = MultipleFieldModel
                search_fields = ['first']
                display_fields = [('first', 'different name'), 'second', ('third', 'The third field')]

        v = TestDirectoryView()
        fields = v.get_display_fields()

        self.assertEqual([
            ('first', 'different name'),
            ('second', 'Second'),
            ('third', 'The third field'),
        ], fields)
