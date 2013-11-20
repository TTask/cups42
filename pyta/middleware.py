from models import RequestHistoryEntry
from models import RequestPriorityEntry
from django.core.exceptions import ObjectDoesNotExist


class RequestStorage():
    def process_request(self, request):
        try:
            priority = RequestPriorityEntry.objects.get(
                request_path=request.path.strip()).request_priority
        except ObjectDoesNotExist:
            priority = 0
        RequestHistoryEntry.objects.create(request_path=request.path,
                                           request_method=request.method,
                                           request_priority=priority)
