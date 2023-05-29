from django.contrib import admin

from .models import Problem, Solution, Comment


admin.site.register(Problem)
admin.site.register(Solution)
admin.site.register(Comment)
