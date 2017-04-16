"""
Views for SymmetricalEureka
"""

from importlib import import_module
try:
    from inspect import signature
except ImportError:
    # pylint: disable=import-error
    from funcsigs import signature

from django.core.exceptions import PermissionDenied, ValidationError
from django.core.urlresolvers import reverse_lazy
from django.db.models import base
from django.http import (Http404, HttpResponseBadRequest, HttpResponseRedirect,
                         JsonResponse)
from django.utils.datastructures import MultiValueDictKeyError
from django.views.generic import DetailView, ListView
from django.views.generic.base import TemplateView, View
from django.views.generic.detail import BaseDetailView

try:
    from django.contrib.auth.mixins import LoginRequiredMixin,\
        PermissionRequiredMixin
except ImportError:
    from SymmetricalEureka.backports.django_contrib_auth_mixins import\
        LoginRequiredMixin, PermissionRequiredMixin

# pylint: disable=wrong-import-order
from rest_framework import generics

from .models import (AbilityScores, CASTER_CLASSES, Character, SpellListing,
                     SpellClasses)
from .forms import AbilityScoresForm, CharacterForm
from .serializers import SpellListingSerializer, SpellClassesSerializer


# pylint: disable=too-many-ancestors
class PlayerLoggedIn(LoginRequiredMixin):
    """
    Class to load header data for logged in user.
    Inherits from LoginRequiredMixin, requiring user to be logged in.
    """
    character_list = None

    def get_context_data(self, **kwargs):
        """
        Override View.get_context_data to add character_list for header.
        """
        self.character_list = Character.objects.filter(
            player=self.request.user).order_by('character_name')
        return super(PlayerLoggedIn, self).get_context_data(**kwargs)


class LoginView(PermissionRequiredMixin, TemplateView):
    """
    Class to display login view.
    We will slightly abuse the notation of the PermissionRequiredMixin.
    The user only has 'permission' for this page if they aren't logged in.
    """
    template_name = 'SymmetricalEureka/login.html'

    def has_permission(self):
        """
        Returns the negation of if the user is authenticated.
        """
        return not self.request.user.is_authenticated()

    def handle_no_permission(self):
        return HttpResponseRedirect(reverse_lazy('SE_home'))

    def get_context_data(self, **kwargs):
        new_kwargs = super(LoginView, self).get_context_data(**kwargs)
        new_kwargs['next_path'] = reverse_lazy('SE_home')
        return new_kwargs


class LoggedInHomeView(PlayerLoggedIn, TemplateView):
    """
    Class to create home page view if logged in.
    """
    template_name = 'SymmetricalEureka/home.html'


class NotLoggedInHomeView(TemplateView):
    """
    Class to create home page view if not logged in.
    """
    template_name = 'SymmetricalEureka/home.html'


class HomeView(View):
    """
    Class to create Home view.
    """
    def get(self, request, *args, **kwargs):
        """
        Split get request into simpler classes.
        """
        if request.user.is_authenticated():
            view = LoggedInHomeView.as_view()
        else:
            view = NotLoggedInHomeView.as_view()

        return view(request, *args, **kwargs)


class DisplayCharacterView(PlayerLoggedIn, DetailView):
    """
    Class for the view to displaying a character.
    """
    template_name = 'SymmetricalEureka/character.html'
    pk_url_kwarg = 'Char_uuid'
    model = Character

    def dispatch(self, request, *args, **kwargs):
        """
        Override TemplateView.dispatch to test if Character belongs to User.
        """
        # pylint: disable=attribute-defined-outside-init
        self.player_character = Character.objects.get(
            Char_uuid=kwargs['Char_uuid'])
        if self.player_character.player.id != request.user.id:
            raise PermissionDenied()
        return super(DisplayCharacterView, self).dispatch(request, *args,
                                                          **kwargs)

    def get_context_data(self, **kwargs):
        kwargs['ability_scores'] = self.get_ability_scores()
        return super(DisplayCharacterView, self).get_context_data(**kwargs)

    def get_ability_scores(self):
        """ generate a list of the ability scores for the character."""
        return AbilityScores.objects.filter(character=self.player_character)


def build_kwargs(func, data):
    """ Build a dictionary of arguments for func out of data."""
    return {x: data.get(x, None) for x in signature(func).parameters.keys()}


class ClassMethodView(View):
    """ Class that exposes classmethods of Django models."""
    module = 'SymmetricalEureka.models'
    extra_methods = {'ability_score_mod': ['abs_saving_throw']}

    def get(self, request, *args, **kwargs):
        """ Handle get requests by passing arguments to classmethod."""
        klass = kwargs['model']
        try:
            cls = getattr(import_module(self.module), klass)
        except AttributeError:
            raise Http404()
        if not issubclass(cls, base.Model):
            raise Http404()
        method = kwargs['method']
        try:
            fnc = getattr(cls, method)
        except AttributeError:
            raise Http404()
        new_kwargs = build_kwargs(fnc, request.GET)
        try:
            result = fnc(**new_kwargs)
        except (TypeError, ValueError):
            return HttpResponseBadRequest()
        response = {method: result}

        for other_method in self.extra_methods.get(method, []):
            try:
                fnc = getattr(cls, other_method)
            except AttributeError:
                fnc = lambda: None
            new_kwargs = build_kwargs(fnc, request.GET)
            try:
                result = fnc(**new_kwargs)
                response[other_method] = result
            except (TypeError, ValueError):
                pass

        return JsonResponse(response)


class CharacterAtributeView(LoginRequiredMixin, BaseDetailView):
    """ View that exposes Character Attributes as JSON api."""
    model = Character
    pk_url_kwarg = 'Char_uuid'
    raise_exception = True
    response_class = JsonResponse

    def get_object(self, queryset=None):
        character = super(CharacterAtributeView, self).get_object(queryset)
        if character.player != self.request.user:
            raise PermissionDenied(self.get_permission_denied_message())
        # pylint: disable=unsubscriptable-object
        attr = AbilityScores.WHICH_ENG_2_KEY.get(self.kwargs['attribute'],
                                                 None)
        queryset = AbilityScores.objects.all().filter(character=character,
                                                      which=attr)
        try:
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404
        return obj

    def render_to_response(self, context, **response_kwargs):
        """ Render a response."""
        obj = context['object']
        response = {AbilityScores.WHICH_KEY_2_ENG[obj.which]: obj.value}
        response.update(response_kwargs)
        return self.response_class(response)

    # pylint: disable=unused-argument
    def post(self, *args, **kwargs):
        """
        Handle post requests by storing to the database and returning the new
        atrribute value.
        """
        # pylint: disable=attribute-defined-outside-init
        self.object = self.get_object()
        request = args[0]
        try:
            val = request.POST['value']
        except MultiValueDictKeyError:
            return HttpResponseBadRequest()
        try:
            # pylint: disable=protected-access
            field = self.object._meta.get_field('value')
            val = field.clean(val, self.object)
        except ValidationError:
            return HttpResponseBadRequest()
        self.object.value = val
        self.object.save()
        func = AbilityScores.ability_score_mod

        context = self.get_context_data(object=self.object)
        return self.render_to_response(context,
                                       ability_score_mod=func(val),
                                       saving_throw=self.object.saving_throw)


class NewCharacterView(PlayerLoggedIn, TemplateView):
    """
    Class for the view to create a new character.
    """
    template_name = 'SymmetricalEureka/new_character.html'

    def get_context_data(self, **kwargs):
        if 'character_form' not in kwargs:
            character_form = CharacterForm(instance=Character())
            kwargs['character_form'] = character_form
        if 'as_forms' not in kwargs:
            as_forms = [AbilityScoresForm(prefix=x[1],
                                          instance=AbilityScores())
                        for x in AbilityScores.WHICH_CHOICES]
            kwargs['as_forms'] = as_forms
        if 'sav_throw' not in kwargs:
            sav_throw = [AbilityScores(which=x[0])
                         for x in AbilityScores.WHICH_CHOICES]
            kwargs['sav_throw'] = sav_throw

        return super(NewCharacterView, self).get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        """ Handle POST requests."""
        character_form = CharacterForm(request.POST, instance=Character())
        as_forms = [AbilityScoresForm(request.POST, prefix=x[1],
                                      instance=AbilityScores())
                    for x in AbilityScores.WHICH_CHOICES]
        if character_form.is_valid() and \
                all([af.is_valid() for af in as_forms]):
            character = character_form.save(commit=False)
            character.player = self.request.user
            character.save()

            for as_form in as_forms:
                ability_score = as_form.save(commit=False)
                ability_score.character = character
                ability_score.which = AbilityScores.WHICH_ENG_2_KEY[
                    as_form.prefix]
                ability_score.save()

            return HttpResponseRedirect(character.get_absolute_url())
        else:
            return self.render_to_response(self.get_context_data(
                character_form=character_form, as_forms=as_forms))


class SpellListView(ListView):
    """
    Class for the view to display Spells.
    """

    model = SpellListing
    template_name = 'SymmetricalEureka/spell_list.html'

    def get_queryset(self):
        return SpellListing.objects.order_by('name')

    def get_context_data(self, **kwargs):
        kwargs['caster_classes'] = CASTER_CLASSES
        return super(SpellListView, self).get_context_data(**kwargs)


class SpellListDetail(generics.RetrieveAPIView):
    """
    Class for the REST API to display Spell details.
    """
    queryset = SpellListing.objects.all()
    serializer_class = SpellListingSerializer


class SpellClassesView(generics.ListAPIView):
    """
    Class for the REST API to display spells by class.
    """
    serializer_class = SpellClassesSerializer

    def get_queryset(self):
        cls = self.kwargs['cls']
        return SpellClasses.objects.filter(caster_class__exact=cls)
