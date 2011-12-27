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

from django.conf import settings

def handler404(request):
    """General 404
    """

    context = {
        
    }
    req_ctx = RequestContext(request, context)

    return render_to_response('404.html', req_ctx)

from django.template import Context, loader

def handler500(request, template_name='500.html'):
    """http://djangosnippets.org/snippets/1199/
    """

    from django.http import HttpResponseServerError
    t = loader.get_template(template_name)
    return HttpResponseServerError(t.render(Context({'MEDIA_URL': settings.MEDIA_URL})))

# EOF

