from django.contrib import admin

from .models import Competition, CompetitionSession, Result

admin.site.register(Result)
admin.site.register(Competition)
admin.site.register(CompetitionSession)
