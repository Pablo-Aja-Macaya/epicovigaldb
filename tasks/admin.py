from django.contrib import admin

from .models import Task
from .models import Team, Team_Component

admin.site.register(Task)
admin.site.register(Team)
admin.site.register(Team_Component)