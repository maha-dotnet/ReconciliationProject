from django.contrib import admin

from .models import (
    SystemARecord,
    SystemBRecord,
    ReconciliationResult
)

admin.site.register(SystemARecord)
admin.site.register(SystemBRecord)
admin.site.register(ReconciliationResult)
