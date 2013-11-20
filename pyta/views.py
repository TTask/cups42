from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.template import RequestContext
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from pyta.forms import EditUserInfoForm
from pyta.forms import EditRequestPriorityForm
from models import UserInfo
from models import RequestHistoryEntry
from models import RequestPriorityEntry
import json


def home_view(request):
    ''' View for index page'''
    user_info = UserInfo.objects.get_or_create(pk=1)[0]
    return render_to_response(
        'index.html',
        {'user_info': user_info},
        context_instance=RequestContext(request))


def requests_view(request):
    ''' First 10 requests view'''
    edit_priority = EditRequestPriorityForm()
    request_entrys = RequestHistoryEntry.objects.all()[:10]
    return render_to_response(
        'requests.html',
        {'first_requests': request_entrys, 'form': edit_priority},
        context_instance=RequestContext(request))


@login_required(login_url='/login')
def edit_view(request):
    '''Edit user info view, allows user to edit data
    represented on the main page'''
    user_info = UserInfo.objects.get_or_create(pk=1)[0]
    if request.method == 'POST':
        edit_form = EditUserInfoForm(request.POST,
                                     request.FILES,
                                     instance=user_info)
        if edit_form.is_valid():
            edit_form.save()
            return redirect(reverse('home'))
        else:
            return render_to_response(
                'edit.html',
                {'edit_form': edit_form},
                context_instance=RequestContext(request))
    else:
        edit_form = EditUserInfoForm(instance=user_info)
        return render_to_response(
            'edit.html',
            {'edit_form': edit_form},
            context_instance=RequestContext(request))


@login_required(login_url='/login')
def edit_view_ajax(request):
    '''This view the same as edit view, but used only if edit form
    submited with ajax'''
    user_info = UserInfo.objects.get_or_create(pk=1)[0]
    if request.method == 'POST' and request.is_ajax():
        response = {}
        edit_form = EditUserInfoForm(
            request.POST,
            request.FILES,
            instance=user_info)
        if edit_form.is_valid():
            edit_form.save()
            response['request_result'] = 'Successfuly saved.'
            return HttpResponse(
                json.dumps(response),
                content_type='application/json')
        else:
            response = dict(
                [field, error] for field, error in edit_form.errors.items())
            response['request_result'] = 'Error occurred'
            return HttpResponse(
                json.dumps(response),
                content_type='application/json')
    else:
        return edit_view(request)


@login_required(login_url='/login')
def set_request_priority_view_ajax(request):
    '''Change request priority'''
    response = {}
    form = EditRequestPriorityForm(request.POST or None)
    if form.is_valid():
        try:
            request_history = RequestHistoryEntry.objects.filter(
                request_path=form.cleaned_data['request_path']).all()
        except ObjectDoesNotExist:
            request_history = []
        priority_entry = RequestPriorityEntry.objects.get_or_create(
            request_path=form.cleaned_data['request_path'])[0]
        priority_entry.request_priority = form.cleaned_data['request_priority']
        priority_entry.save()
        for http_req in request_history:
            http_req.request_priority = form.cleaned_data['request_priority']
            http_req.save()
        response['request_result'] = 'Priority changed successfull'
        return HttpResponse(json.dumps(response),
            content_type='application/json')
    else:
        response = dict(
            [field, error] for field,error in form.errors.items())
        response['request_result'] = 'Error occurred'
        return HttpResponse(json.dumps(response),
            content_type='application/json')




