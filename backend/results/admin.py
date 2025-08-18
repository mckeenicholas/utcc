from django.contrib import admin
from .models import CompetitionSession, Result, Competition

admin.site.register(Result)
admin.site.register(Competition)
admin.site.register(CompetitionSession)
