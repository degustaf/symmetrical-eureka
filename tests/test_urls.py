# pylint: disable=missing-docstring

from uuid import uuid4

from django import VERSION
# from django.contrib.auth.models import User
# from django.contrib.auth.views import login
from django.core.urlresolvers import resolve, reverse
from django.test import TestCase
from social_django import views as social_views

from SymmetricalEureka import views

# For url testing class based views:
# http://stackoverflow.com/questions/27320821/django-how-to-assert-url-pattern-resolves-to-correct-class-based-view-function
# Or use pdb.setbreak.


class UrlTest(TestCase):

    def test_home_url_resolves(self):
        found = resolve(reverse('SE_home'))
        self.assertEqual(found.func.__name__, views.HomeView.__name__)

    def test_social_urls_resolve(self):
        found = resolve(reverse('social:begin', kwargs={'backend': 'TEST'}))
        self.assertEqual(found.func, social_views.auth)

    def test_auth_urls_resolve(self):
        found = resolve(reverse('auth:logout'))
        if VERSION < (1, 11):
            from django.contrib.auth.views import logout
            self.assertEqual(found.func, logout)
        else:
            from django.contrib.auth.views import LogoutView
            self.assertEqual(found.func.__name__, LogoutView.__name__)

    def test_character_urls_resolve(self):
        found = resolve(reverse('SE_character',
                                kwargs={'Char_uuid': uuid4()}))
        self.assertEqual(found.func.__name__,
                         views.DisplayCharacterView.__name__)

    def test_new_character_url_resolves(self):
        found = resolve(reverse('new_character'))
        self.assertEqual(found.func.__name__, views.NewCharacterView.__name__)

    def test_spell_list_url_resolves(self):
        found = resolve(reverse('SE_spell_list'))
        self.assertEqual(found.func.__name__, views.SpellListView.__name__)

    def test_login_page_resolves(self):
        found = resolve(reverse('SE_login'))
        self.assertEqual(found.func.__name__, views.LoginView.__name__)

    def test_user_spell_resolves(self):
        found = resolve(reverse('UserSpell', kwargs={'pk': 'Aid'}))
        self.assertEqual(found.func.__name__, views.UserSpellView.__name__)

    def test_empty_user_spell_resolves(self):
        found = resolve(reverse('UserSpell', kwargs={'pk': ''}))
        self.assertEqual(found.func.__name__, views.UserSpellView.__name__)

    def test_spell_class_resolves(self):
        found = resolve(reverse('SE_spell_class', kwargs={'cls': 'pd'}))
        self.assertEqual(found.func.__name__, views.SpellClassesView.__name__)

    def test_empty_spell_class_resolves(self):
        found = resolve(reverse('SE_spell_class', kwargs={'cls': ''}))
        self.assertEqual(found.func.__name__, views.SpellClassesView.__name__)
