"""
Views for SymmetricalEureka
"""


from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template.context import RequestContext

from SymmetricalEureka.models import Character


def home(request):
    """
    View for the home page.
    """
    character_list = None
    if request.user.is_authenticated():
        character_list = Character.objects.filter(
            player=request.user).order_by('Name')
    context = RequestContext(request, {'request': request,
                                       'user': request.user,
                                       'character_list': character_list})
    return render_to_response('SymmetricalEureka/home.html',
                              context_instance=context)


def login(request):
    """
    View for the login page.
    """
    if request.user.is_authenticated():
        return redirect('SE_home')
    # return render_to_response('SymmetricalEureka/login.html')

    context = RequestContext(request, {'next_path': reverse_lazy('SE_home')})
    return render_to_response('SymmetricalEureka/login.html',
                              context_instance=context)


@login_required
def display_character(request, character_uuid):
    """
    View to display a Character.
    """
    player_character = Character.objects.get(Char_uuid=character_uuid)
    if player_character.player.id == request.user.id:
        character_list = Character.objects.filter(
            player=request.user).order_by('Name')
        context = RequestContext(request,
                                 {'request': request,
                                  'user': request.user,
                                  'character_list': character_list,
                                  'player_character': player_character})
        return render_to_response('SymmetricalEureka/home.html',
                                  context_instance=context)

    return HttpResponse("Unauthorized", status=401)


@login_required
# pylint: disable=unused-argument
def new_character(request):
    """
    View to create a new character.
    """
    if request.method == 'GET':
        return render_to_response('SymmetricalEureka/new_character.html')
    if request.method == 'POST':
        return HttpResponse("")
