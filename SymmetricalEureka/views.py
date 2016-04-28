"""
Views for SymmetricalEureka
"""


from django.shortcuts import render_to_response
from django.template.context import RequestContext


def home(request):
    """
    View for the home page.
    """
    context = RequestContext(request, {'request': request,
                                       'user': request.user})
    return render_to_response('SymmetricalEureka/home.html',
                              context_instance=context)
