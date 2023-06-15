from django.contrib import admin

from .models import Study, Studying, Announcement, AnnouncementRead, StudyComment

# Register your models here.
admin.site.register(Study)
admin.site.register(Studying)
admin.site.register(Announcement)
admin.site.register(AnnouncementRead)
admin.site.register(StudyComment)