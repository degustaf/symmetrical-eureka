"""
SymmetricalEureka URL Configuration
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import urls as auth_urls
from social_django import urls as social_urls
from SymmetricalEureka import views


admin.autodiscover()

# pylint: disable=invalid-name
char_uuid_regex = r'[-0-9a-f]{36}'
model_regex = r'[A-Z][a-zA-Z0-9]+'
attribute_regex = r'[a-z_][a-z0-9_]{2,30}'
urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='SE_home'),
    url(r'^login/$', views.LoginView.as_view(), name='SE_login'),
    url(r'^character/(?P<Char_uuid>{})/$'.format(char_uuid_regex),
        views.DisplayCharacterView.as_view(), name='SE_character'),
    url(r'^new_character/', views.NewCharacterView.as_view(),
        name='new_character'),
    url(r'^api/(?P<model>{})/(?P<method>{})$'.format(
        model_regex, attribute_regex),
        views.ClassMethodView.as_view(), name='SE_ClassMethod'),
    url(r'^api/(?P<Char_uuid>{})/AbilityScores/(?P<attribute>{})$'.format(
        char_uuid_regex, attribute_regex),
        views.CharacterAtributeView.as_view(), name='SE_character_method'),
    url(r'^spells/$', views.SpellListView.as_view(), name='SE_spell_list'),
    url(r'^api/spells/'),   # TODO how to define this API endpoint for UserSpellView????
    url(r'^spells/(?P<pk>.+)$', views.SpellListDetail.as_view(),
        name='SE_spell_detail'),
    url(r'^class/(?P<cls>.*)$', views.SpellClassesView.as_view(),
        name='SE_spell_class'),
    url('', include(social_urls, namespace='social')),
    url('', include(auth_urls, namespace='auth')),
]
