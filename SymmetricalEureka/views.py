"""
Views for SymmetricalEureka
"""


from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render_to_response, redirect
from django.template.context import RequestContext


def home(request):
    """
    View for the home page.
    """
    context = RequestContext(request, {'request': request,
                                       'user': request.user})
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
