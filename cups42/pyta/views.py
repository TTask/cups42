from django.shortcuts import render
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.template import RequestContext
from models import UserInfo
from models import RequestHistoryEntry


def home_view(request):
    user_info = UserInfo.objects.get_or_create(pk=1)[0]
    return render_to_response('index.html', {'user_info': user_info}, 
        context_instance=RequestContext(request))


def login_view(request):
    pass


def logout_view(request):
    pass


def edit_view(request):
    pass


def requests_view(request):
    request_entrys = RequestHistoryEntry.objects.all()[:10]
    return render_to_response('requests.html', {'first_requests' : request_entrys}, 
        context_instance=RequestContext(request))

