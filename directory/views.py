from copy import copy
from django import forms
from django.core.exceptions import ImproperlyConfigured
from django.views.generic import ListView
import six as six
from .filters import generate_model_filter_class


class DirectoryOptions(object):
    def __init__(self, options):
        self.abstract = getattr(options, 'abstract', False)

        self.basic_filter_class = getattr(options, 'filter_class', None)
        self.basic_search_fields = getattr(options, 'search_fields', None)
        self.display_headings = getattr(options, 'display_headings', True)
        self.form_class = getattr(options, 'form_class', None)

        if self.basic_filter_class:
            self.model = self.basic_filter_class.Meta.model
        else:
            self.model = getattr(options, 'model', None)

        if not self.basic_filter_class and not self.model and not self.abstract:
            raise ImproperlyConfigured('Neither Meta.filter_class nor Meta.model were set')

        self.display_fields = []
        if self.model:
            for f in getattr(options, 'display_fields', sorted(self.model._meta.get_all_field_names())):
                if isinstance(f, six.string_types):
                    field_name = f
                    verbose_name = self.model._meta.get_field(f).verbose_name.title()
                else:
                    field_name = f[0]
                    verbose_name = f[1]
                self.display_fields.append((field_name, verbose_name))

        if self.display_fields:
            self.link_on_field = getattr(options, 'link_on_field', self.display_fields[0][0])


class DirectoryViewMetaclass(type):
    def __new__(cls, name, bases, attrs):
        new_class = super(DirectoryViewMetaclass, cls).__new__(cls, name, bases, attrs)

        new_class._meta = DirectoryOptions(new_class.Meta)

        return new_class


class BaseDirectoryView(ListView):
    unfiltered_queryset = None
    template_name = 'directory/base.html'

    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        if self._meta.abstract:
            raise ImproperlyConfigured('You cannot create and instance of an abstract DirectoryView')

        self._filter = None

        super(BaseDirectoryView, self).__init__(*args, **kwargs)

    def get_filter_class(self):
        if not self._meta.basic_filter_class:
            return generate_model_filter_class(
                self._meta.model,
                self.get_search_fields(),
                self.get_form_class()
            )
        return self._meta.basic_filter_class

    def get_filter(self):
        if self._filter is None:
            self._filter = self.get_filter_class()(data=self.request.GET, queryset=self.get_unfiltered_queryset())

        return self._filter

    def get_form_class(self):
        return self._meta.form_class

    def get_unfiltered_queryset(self):
        if self.unfiltered_queryset is None:
            return self._meta.model._default_manager.all()

        return self.unfiltered_queryset

    def get_queryset(self):
        return self.get_filter().qs

    def get_context_data(self, **kwargs):
        kwargs.setdefault('filter', self.get_filter())

        field_names, headings = zip(*self.get_display_fields())
        kwargs.setdefault('field_names', field_names)
        kwargs.setdefault('field_headings', headings)

        kwargs.setdefault('display_headings', self._meta.display_headings)
        kwargs.setdefault('link_on_field', self._meta.link_on_field)

        qs = copy(self.request.GET)
        if 'page' in qs:
            del qs['page']

        kwargs.setdefault('filter_query_string', qs.urlencode())

        return super(BaseDirectoryView, self).get_context_data(**kwargs)

    def get_display_fields(self):
        return self._meta.display_fields

    def get_search_fields(self):
        if not self._meta.basic_search_fields:
            raise ImproperlyConfigured('Neither Meta.search_fields nor Meta.filter_class were set')

        return self._meta.basic_search_fields


class DirectoryView(six.with_metaclass(DirectoryViewMetaclass, BaseDirectoryView)):
    pass
