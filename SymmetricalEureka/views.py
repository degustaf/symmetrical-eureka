"""
Views for SymmetricalEureka
"""

from collections import OrderedDict
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
from django.views.generic import DetailView
from django.views.generic.base import TemplateView, View
from django.views.generic.detail import BaseDetailView

try:
    from django.contrib.auth.mixins import LoginRequiredMixin,\
        PermissionRequiredMixin
except ImportError:
    from SymmetricalEureka.backports.django_contrib_auth_mixins import\
        LoginRequiredMixin, PermissionRequiredMixin

from .models import AbilityScores, Character, Skills
from .forms import AbilityScoresForm, CharacterForm, SkillsForm


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
    return {k: data.get(k, None if v.default == v.empty else v.default)
            for k, v in signature(func).parameters.items()}


class ClassMethodView(View):
    """ Class that exposes classmethods of Django models."""
    module = 'SymmetricalEureka.models'
    extra_methods = {'ability_score_mod': ['abs_saving_throw',
                                           'abs_skills_bonus']}

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
        if 'skills_forms' not in kwargs:
            skills_forms = [SkillsForm(prefix=x[0], instance=Skills())
                            for x in Skills.CHOICES]
            kwargs['skills_forms'] = skills_forms

        return super(NewCharacterView, self).get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        """ Handle POST requests."""
        forms = self.get_forms(request.POST)
        if self.is_valid(forms):
            return self.form_valid(forms)
        else:
            return self.render_to_response(self.get_context_data(**forms))

    def form_valid(self, forms):
        """ Process forms after it is determined that they are valid."""
        character = forms['character_form'].save(commit=False)
        character.player = self.request.user
        character.save()

        ability_scores = {}
        for as_form in forms['as_forms']:
            key = AbilityScores.WHICH_ENG_2_KEY[as_form.prefix]
            ability_scores[key] = as_form.save(commit=False)
            ability_scores[key].character = character
            ability_scores[key].which = key

            ability_scores[key].save()

        for skills_form in forms['skills_forms']:
            skill = skills_form.save(commit=False)
            skill.which = skills_form.prefix
            key = Skills.SKILLS_2_ABILITY_SCORES[skills_form.prefix]
            skill.ability_score = ability_scores[key]

            skill.save()

        return HttpResponseRedirect(character.get_absolute_url())

    # pylint: disable=no-self-use
    def get_forms(self, data):
        """ Construct forms."""
        response = OrderedDict()
        response['character_form'] = CharacterForm(data, instance=Character())
        response['as_forms'] = [AbilityScoresForm(data, prefix=x[1],
                                                  instance=AbilityScores())
                                for x in AbilityScores.WHICH_CHOICES]
        response['skills_forms'] = [SkillsForm(data, prefix=x[0],
                                               instance=Skills())
                                    for x in Skills.CHOICES]
        return response

    def is_valid(self, forms_dict):
        """ validate forms in forms_dict."""
        for item in forms_dict.values():
            if isinstance(item, list):
                if not all([x.is_valid() for x in item]):
                    return False
            else:
                if not item.is_valid():
                    return False

        return True
