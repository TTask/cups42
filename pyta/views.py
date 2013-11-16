from django.shortcuts import render
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from models import UserInfo
from models import RequestHistoryEntry
from pyta.forms import EditUserInfoForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import json


def home_view(request):
    user_info = UserInfo.objects.get_or_create(pk=1)[0]
    return render_to_response('index.html', {'user_info': user_info}, 
        context_instance=RequestContext(request))


def requests_view(request):
    request_entrys = RequestHistoryEntry.objects.all()[:10]
    return render_to_response('requests.html', {'first_requests' : request_entrys}, 
        context_instance=RequestContext(request))


@login_required(login_url='/login')
def edit_view(request):
	user_info = UserInfo.objects.get_or_create(pk=1)[0]
	if request.method == 'POST':
		edit_form = EditUserInfoForm(request.POST, request.FILES, instance=user_info)		
		if edit_form.is_valid():
			edit_form.save()
			return redirect(reverse('home'))
		else:
			return render_to_response('edit.html', {'edit_form' : edit_form}, 
				context_instance=RequestContext(request))
	else:
		edit_form = EditUserInfoForm(instance=user_info)
		return render_to_response('edit.html', {'edit_form' : edit_form}, 
			context_instance=RequestContext(request))


@login_required()
def edit_view_ajax(request):
	if request.method == 'POST' and request.is_ajax():
		curr_user = UserInfo.objects.get_or_create(pk=1)[0]
		form = EditUserInfoForm(request.POST, request.FILES, instance=curr_user)
		print(request.POST)
		if form.is_valid():
			form.save()
			response_data = {}
			response_data['result'] = 'success'
			response_data['message'] = 'Successfuly saved.'
			return HttpResponse(json.dumps(response_data), content_type="application/json", 
				context_instance=RequestContext(request))
		else:
			response_data = {}
			for key, val in form.errors:
				response_data[key] = val
			return HttpResponse(json.dumps(response_data), content_type="application/json")

	else:
		return HttpResponse("Ajax only submiting", content_type="text/plain")
		


