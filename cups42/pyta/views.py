from django.shortcuts import render
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.template import RequestContext
from models import UserInfo
from models import RequestHistoryEntry
from forms import EditUserInfoForm


def home_view(request):
    user_info = UserInfo.objects.get_or_create(pk=1)[0]
    return render_to_response('index.html', {'user_info': user_info}, 
        context_instance=RequestContext(request))


def login_view(request):
    pass


def logout_view(request):
    pass


def requests_view(request):
    request_entrys = RequestHistoryEntry.objects.all()[:10]
    return render_to_response('requests.html', {'first_requests' : request_entrys}, 
        context_instance=RequestContext(request))

def edit_view(request):
	user_info = UserInfo.objects.get_or_create(pk=1)[0]
	edit_form = EditUserInfoForm(request.POST or None, 
		request.FILES or None, instance=user_info)
	if edit_form.is_valid():
		edit_form.save()
	else:
		return render_to_response('edit.html', {'edit_form' : edit_form}, 
			context_instance=RequestContext(request))