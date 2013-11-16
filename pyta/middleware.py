from models import RequestHistoryEntry


class RequestStorage():
    def process_request(self, request):
        RequestHistoryEntry.objects.create(request_path=request.path, 
            request_method=request.method)
