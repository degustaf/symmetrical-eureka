"""
Views for SymmetricalEureka
"""


from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, DetailView
from django.views.generic.base import TemplateView, View

try:
    from django.contrib.auth.mixins import LoginRequiredMixin,\
        PermissionRequiredMixin
except ImportError:
    from SymmetricalEureka.backports.django_contrib_auth_mixins import\
        LoginRequiredMixin, PermissionRequiredMixin

from SymmetricalEureka.models import Character


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


# class DisplayCharacterView(PlayerLoggedIn, TemplateView):
#     """
#     Class for the view to displaying a character.
#     """
#     template_name = 'SymmetricalEureka/character.html'
#     player_character = None

#     def dispatch(self, request, *args, **kwargs):
#         """
#         Override TemplateView.dispatch to test if Character belongs to User.
#         """
#         self.player_character = Character.objects.get(
#             Char_uuid=kwargs['character_uuid'])
#         if self.player_character.player.id != request.user.id:
#             raise PermissionDenied()
#         return super(DisplayCharacterView, self).dispatch(request, *args,
#                                                           **kwargs)

class DisplayCharacterView(PlayerLoggedIn, DetailView):
    """
    Class for the view to displaying a character.
    """
    template_name = 'SymmetricalEureka/character.html'
    pk_url_kwarg = 'Char_uuid'
    queryset = Character.objects.all()

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


class NewCharacterView(PlayerLoggedIn, CreateView):
    """
    Class for the view to create a new character.
    """
    template_name = 'SymmetricalEureka/new_character.html'
    model = Character
    fields = ['character_name', 'alignment']

    def form_valid(self, form):
        """
        Override form_valid() to insert player for the model.
        """
        # pylint: disable=attribute-defined-outside-init
        self.object = form.save(commit=False)
        self.object.player = self.request.user
        self.object.save()
        return super(NewCharacterView, self).form_valid(form)
