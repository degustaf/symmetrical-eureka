"""
Classes to test templates.
"""

from django.contrib.auth.models import User
# from django.contrib.auth.views import login
from django.core.urlresolvers import reverse
from django.test import TestCase

from SymmetricalEureka.models import Character


class OneUserTemplateTests(TestCase):
    """
    Class of tests for the New Character page.
    """
    fixtures = ['user_mike.json']

    @classmethod
    def setUpTestData(cls):
        """
        Initialize database for tests.
        """
        # pylint: disable=no-member
        cls.test_user = User.objects.get(username="Mike")

    def setUp(self):
        """
        Log user in.
        """
        try:
            self.client.force_login(self.test_user)
        except AttributeError:
            # For Django 1.8
            self.client.login(username="Mike", password="password")

    def test_has_form(self):
        """
        Test that new character page responds.
        """
        response = self.client.get(reverse('new_character'))
        self.assertContains(response, 'html')
        self.assertContains(response, 'Create New Character')
        self.assertContains(response, 'form')
        self.assertContains(response, 'method="post"')
        self.assertContains(response, 'submit')
        self.assertContains(response, 'select')

    def test_form_has_name(self):
        """
        Test that new character page has a place for character name.
        """
        response = self.client.get(reverse('new_character'))
        self.assertContains(response, 'Character name')

    def test_form_has_alignment(self):
        """
        Test that new character page has alignment field.
        """
        response = self.client.get(reverse('new_character'))
        self.assertContains(response, 'alignment')

    def test_form_has_ability_scores(self):
        """
        Test that new character page has ability scores.
        """
        response = self.client.get(reverse('new_character'))
        self.assertContains(response, 'Strength')
        self.assertContains(response, 'Dexterity')
        self.assertContains(response, 'Constitution')
        self.assertContains(response, 'Intelligence')
        self.assertContains(response, 'Wisdom')
        self.assertContains(response, 'Charisma')

    def test_homepage_has_new_char_link(self):
        """
        Test that homepage has link to new_character page.
        """
        response = self.client.get(reverse('SE_home'))
        self.assertContains(response, reverse('new_character'))


class OneCharTemplateTests(TestCase):
    """ Class of tests for the New Character page."""
    fixtures = ['user_mike.json', 'zeke.json']

    @classmethod
    def setUpTestData(cls):
        """ Initialize database for tests."""
        # pylint: disable=no-member
        cls.test_user = User.objects.get(username="Mike")
        cls.test_character = Character.objects.get(character_name="Zeke")
        cls.test_character.save()
        cls.test_url = reverse('SE_character', kwargs={
            'Char_uuid': cls.test_character.Char_uuid})

    def setUp(self):
        """ Log user in."""
        try:
            self.client.force_login(self.test_user)
        except AttributeError:
            # For Django 1.8
            self.client.login(username="Mike", password="password")

    def test_character_shows_in_header(self):
        """ Test that character shows on homepage."""
        response = self.client.get(reverse('SE_home'))
        self.assertContains(response, self.test_character.character_name)
        self.assertContains(response, self.test_url)
        self.assertContains(response, self.test_character.character_name)

    def test_character_shows_as_title(self):
        """ Test that character name appears as title in h1 block."""
        response = self.client.get(self.test_url)
        self.assertContains(response, '<h1>{}</h1>'.format(
            self.test_character.character_name))

    def test_alignment_shows(self):
        """ Test that alignment displays on character page."""
        response = self.client.get(self.test_url)
        self.assertContains(response, 'Alignment')

    def test_ability_scores_show(self):
        """ Test that ability scores display on character page."""
        response = self.client.get(self.test_url)
        self.assertContains(response, 'Strength')
        self.assertContains(response, self.test_character.strength)
        self.assertContains(response, Character.ability_score_mod(
            self.test_character.strength))
        self.assertContains(response, 'Dexterity')
        self.assertContains(response, self.test_character.dexterity)
        self.assertContains(response, 'Constitution')
        self.assertContains(response, self.test_character.constitution)
        self.assertContains(response, 'Intelligence')
        self.assertContains(response, self.test_character.intelligence)
        self.assertContains(response, 'Wisdom')
        self.assertContains(response, self.test_character.wisdom)
        self.assertContains(response, 'Charisma')
        self.assertContains(response, self.test_character.charisma)

    def test_uuid_appears(self):
        """ Test that uuid is present in page."""
        response = self.client.get(self.test_url)
        expected_result = '<div class="hidden" id="uuid">{}</div>'.format(
            self.test_character.Char_uuid)
        self.assertContains(response, expected_result)

    def test_logout_redirects_to_home(self):
        """
        Test that after user is logged out, they are redirected to the home
        page.
        """
        response = self.client.get(self.test_url)
        expected_result = "{}?next={}".format(reverse("auth:logout"),
                                              reverse("SE_home"))
        self.assertContains(response, expected_result)
