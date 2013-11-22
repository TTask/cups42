from django.shortcuts import render
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from models import UserInfo
from models import RequestHistoryEntry
from forms import EditUserInfoForm


def home_view(request):
    user_info = UserInfo.objects.get_or_create(pk=1)[0]
    return render_to_response(
        'index.html',
        {'user_info': user_info},
        context_instance=RequestContext(request))


def requests_view(request):
    request_entrys = RequestHistoryEntry.objects.all()[:10]
    return render_to_response(
        'requests.html',
        {'first_requests': request_entrys},
        context_instance=RequestContext(request))


@login_required(login_url='/login')
def edit_view(request):
    user_info = UserInfo.objects.get_or_create(pk=1)[0]
    if request.method == 'GET':
        edit_form = EditUserInfoForm(instance=user_info)
        return render_to_response('edit.html', {'edit_form': edit_form},
                                  context_instance=RequestContext(request))
    edit_form = EditUserInfoForm(request.POST or None,
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
