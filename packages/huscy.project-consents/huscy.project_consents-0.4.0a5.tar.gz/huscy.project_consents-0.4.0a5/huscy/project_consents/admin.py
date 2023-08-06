from django.contrib import admin

from .models import ProjectConsent, ProjectConsentCategory, ProjectConsentFile


admin.site.register(ProjectConsent)
admin.site.register(ProjectConsentCategory)
admin.site.register(ProjectConsentFile)
