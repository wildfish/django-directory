from django.test import TestCase
from directory.templatetags.directory_utils import get_selectable_pages


class FakePage(object):
    class FakePaginator(object):
        def __init__(self, total_num_pages):
            self.num_pages = total_num_pages
            self.page_range = [i for i in range(1, total_num_pages + 1)]

    def __init__(self, current_page, total_num_pages):
        self.number = current_page
        self.paginator = self.FakePaginator(total_num_pages)


class TemplateTagsGetSelectablePages(TestCase):
    def test_there_are_less_pages_in_the_paginator_than_are_allowed_in_the_limit___all_pages_are_returned(self):
        page = FakePage(1, 5)

        selectable_pages = get_selectable_pages(page, 1)

        self.assertEqual([1, 2, 3, 4, 5], selectable_pages)

    def test_there_are_more_pages_in_the_paginator_than_are_allowed_in_the_limit_and_we_are_near_the_start___pages_up_to_the_limit_are_returned_with_break_before_final_page(self):
        page = FakePage(3, 6)

        selectable_pages = get_selectable_pages(page, 1)

        self.assertEqual([1, 2, 3, 4, None, 6], selectable_pages)

    def test_there_are_more_pages_in_the_paginator_than_are_allowed_in_the_limit_and_we_are_near_the_end___first_page_then_a_break_then_pages_in_the_limit_to_the_end_are_returned(self):
        page = FakePage(4, 6)

        selectable_pages = get_selectable_pages(page, 1)

        self.assertEqual([1, None, 3, 4, 5, 6], selectable_pages)

    def test_there_are_more_pages_in_the_paginator_than_are_allowed_in_the_limit_and_we_are_in_the_middle___first_page_then_a_break_followed_byt_the_pages_in_the_limit_then_a_break_and_final_are_returned(self):
        page = FakePage(4, 7)

        selectable_pages = get_selectable_pages(page, 1)

        self.assertEqual([1, None, 3, 4, 5, None, 7], selectable_pages)
