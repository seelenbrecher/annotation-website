from django.contrib import admin

# Register your models here.
from .models import Database, Claim, Evidence, TemporalClaimSection, Annotation, Justification

admin.site.register(Database)
admin.site.register(Claim)
admin.site.register(Evidence)
admin.site.register(TemporalClaimSection)

admin.site.register(Annotation)
admin.site.register(Justification)