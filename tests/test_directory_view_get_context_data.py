from django.test import TestCase, RequestFactory
from directory.views import DirectoryView
from .models import TestModelB, MultipleFieldModel


class DirectoryViewGetContextData(TestCase):
    def test_filter_is_not_supplied_in_kwargs___filter_is_added(self):
        class TestDirectoryView(DirectoryView):
            class Meta:
                model = TestModelB
                search_fields = ['field_b']

        v = TestDirectoryView()
        v.request = RequestFactory().get('/')
        v.object_list = []

        context_data = v.get_context_data()

        self.assertEqual(v.get_filter(), context_data['filter'])

    def test_filter_is_supplied_in_kwargs___filter_is_not_changed(self):
        class TestDirectoryView(DirectoryView):
            class Meta:
                model = TestModelB
                search_fields = ['field_b']

        v = TestDirectoryView()
        v.request = RequestFactory().get('/')
        v.object_list = []

        context_data = v.get_context_data(filter='some filter')

        self.assertEqual('some filter', context_data['filter'])

    def test_field_names_are_not_supplied_in_kwargs___field_names_are_added(self):
        class TestDirectoryView(DirectoryView):
            class Meta:
                model = TestModelB
                search_fields = ['field_b']

        v = TestDirectoryView()
        v.request = RequestFactory().get('/')
        v.object_list = []

        context_data = v.get_context_data()

        self.assertEqual(('id', 'field_b'), context_data['field_names'])

    def test_field_names_are_supplied_in_kwargs___field_names_are_not_changed(self):
        class TestDirectoryView(DirectoryView):
            class Meta:
                model = TestModelB
                search_fields = ['field_b']

        v = TestDirectoryView()
        v.request = RequestFactory().get('/')
        v.object_list = []

        context_data = v.get_context_data(field_names=['some name'])

        self.assertEqual(['some name'], context_data['field_names'])

    def test_field_headings_are_not_supplied_in_kwargs___field_headings_are_added(self):
        class TestDirectoryView(DirectoryView):
            class Meta:
                model = TestModelB
                search_fields = ['field_b']

        v = TestDirectoryView()
        v.request = RequestFactory().get('/')
        v.object_list = []

        context_data = v.get_context_data()

        self.assertEqual(('Id', 'Field B'), context_data['field_headings'])

    def test_field_headings_are_supplied_in_kwargs___field_names_are_not_changed(self):
        class TestDirectoryView(DirectoryView):
            class Meta:
                model = TestModelB
                search_fields = ['field_b']

        v = TestDirectoryView()
        v.request = RequestFactory().get('/')
        v.object_list = []

        context_data = v.get_context_data(field_headings=['some heading'])

        self.assertEqual(['some heading'], context_data['field_headings'])

    def test_display_headings_is_not_supplied_in_kwargs_or_meta___display_headings_is_true(self):
        class TestDirectoryView(DirectoryView):
            class Meta:
                model = TestModelB
                search_fields = ['field_b']

        v = TestDirectoryView()
        v.request = RequestFactory().get('/')
        v.object_list = []

        context_data = v.get_context_data()

        self.assertTrue(context_data['display_headings'])

    def test_display_headings_is_not_supplied_in_kwargs_but_is_on_meta___display_headings_matches_meta(self):
        class TestDirectoryView(DirectoryView):
            class Meta:
                model = TestModelB
                search_fields = ['field_b']
                display_headings = False

        v = TestDirectoryView()
        v.request = RequestFactory().get('/')
        v.object_list = []

        context_data = v.get_context_data()

        self.assertFalse(context_data['display_headings'])

    def test_display_headings_is_supplied_in_kwargs___display_headings_matches_the_kwargs(self):
        class TestDirectoryView(DirectoryView):
            class Meta:
                model = TestModelB
                search_fields = ['field_b']
                display_headings = False

        v = TestDirectoryView()
        v.request = RequestFactory().get('/')
        v.object_list = []

        context_data = v.get_context_data(display_headings=True)

        self.assertTrue(context_data['display_headings'])

    def test_link_on_field_is_not_supplied_in_kwargs_or_meta___link_on_field_is_first_field(self):
        class TestDirectoryView(DirectoryView):
            class Meta:
                model = MultipleFieldModel
                search_fields = ['first']
                display_headings = False

        v = TestDirectoryView()
        v.request = RequestFactory().get('/')
        v.object_list = []

        context_data = v.get_context_data()

        self.assertEqual(context_data['field_names'][0], context_data['link_on_field'])

    def test_link_on_field_is_not_supplied_in_kwargs_but_is_on_meta___link_on_field_is_field_in_meta(self):
        class TestDirectoryView(DirectoryView):
            class Meta:
                model = MultipleFieldModel
                search_fields = ['first']
                display_headings = False
                link_on_field = 'second'

        v = TestDirectoryView()
        v.request = RequestFactory().get('/')
        v.object_list = []

        context_data = v.get_context_data()

        self.assertEqual('second', context_data['link_on_field'])

    def test_link_on_field_is_not_supplied_in_kwargs_but_is_on_meta_as_none___link_on_field_is_none(self):
        class TestDirectoryView(DirectoryView):
            class Meta:
                model = MultipleFieldModel
                search_fields = ['first']
                display_headings = False
                link_on_field = None

        v = TestDirectoryView()
        v.request = RequestFactory().get('/')
        v.object_list = []

        context_data = v.get_context_data()

        self.assertIsNone(context_data['link_on_field'])

    def test_link_on_field_is_supplied_in_kwargs___link_on_field_matches_the_kwargs(self):
        class TestDirectoryView(DirectoryView):
            class Meta:
                model = MultipleFieldModel
                search_fields = ['first']
                display_headings = False
                link_on_field = None

        v = TestDirectoryView()
        v.request = RequestFactory().get('/')
        v.object_list = []

        context_data = v.get_context_data(link_on_field='third')

        self.assertEqual('third', context_data['link_on_field'])
