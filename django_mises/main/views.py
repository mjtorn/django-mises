# vim: tabstop=4 expandtab autoindent shiftwidth=4 fileencoding=utf-8

from django.template import RequestContext

from django.shortcuts import render_to_response

def index(request):
    """Index view
    """

    context = {
        
    }
    req_ctx = RequestContext(request, context)

    return render_to_response('index.html', req_ctx)

# EOF

