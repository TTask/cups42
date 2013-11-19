from django.contrib import admin
from models import UserInfo
from models import RequestHistoryEntry
from models import ModelHistoryEntry


admin.site.register(UserInfo)
admin.site.register(RequestHistoryEntry)
admin.site.register(ModelHistoryEntry)
