from django.views.generic import View

from directory.templatetags import directory_utils as tags
from unittest import TestCase


class TemplateTagsrender(TestCase):
    def setUp(self):
        self.context = {
            'view': View()
        }

    def test_object_does_not_have_the_attribute_no_default_is_set___empty_string_is_returned(self):
        class A(object):
            foo = 'bar'

        res = tags.render(self.context, A(), 'bar')

        self.assertEqual('', res)

    def test_object_does_not_have_the_attribute_default_is_set___default_is_returned(self):
        class A(object):
            foo = 'bar'

        res = tags.render(self.context, A(), 'bar,boo')

        self.assertEqual('boo', res)

    def test_object_has_the_attribute___attribute_value_is_returned(self):
        class A(object):
            foo = 'bar'

        res = tags.render(self.context, A(), 'foo,boo')

        self.assertEqual('bar', res)

    def test_object_has_the_attribute_which_is_callable___attribute_return_value_is_returned(self):
        class A(object):
            def foo(self):
                return 'bar'

        res = tags.render(self.context, A(), 'foo,boo')

        self.assertEqual('bar', res)

    def test_object_has_the_render_attribute_which_is_callable___attribute_return_value_is_returned(self):
        self.context['view'].render_foo = lambda x: 'bar'

        class A(object):
            pass

        res = tags.render(self.context, A(), 'foo,boo')

        self.assertEqual('bar', res)
