from django.core.paginator import Paginator 
from django.shortcuts import render_to_response, get_object_or_404, HttpResponseRedirect 
from django.template import RequestContext 
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponsePermanentRedirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


def home(request):
  return render_to_response('home.html', locals(), context_instance=RequestContext(request))
