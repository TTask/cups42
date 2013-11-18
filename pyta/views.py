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


@login_required(login_url="/login")
def edit_view_ajax(request):
	user_info = UserInfo.objects.get_or_create(pk=1)[0]
	if request.method == 'POST' and request.is_ajax():
		response = {}
		edit_form = EditUserInfoForm(request.POST, request.FILES, instance=user_info)
		if edit_form.is_valid():
			edit_form.save()
			response['result']  = 'Successfuly saved.'
			return HttpResponse(json.dumps(response), content_type='application/json', 
				context_instance=RequestContext(request))
		else:
			response = dict([field, error] for field, error in edit_form.errors)
			return HttpResponse(json.dumps(response), content_type='application/json', 
				context_instance=RequestContext(request))

	else: 
		return edit_view(request)