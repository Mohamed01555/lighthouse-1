from django.contrib import admin
from .models import (
    UnKnownMissingPerson,
    KnownMissingPerson,
    UserSeeKnownMissingPerson,
    UserSeeUnknownMissingPerson,
    KnownMissingPersonImages,
)

admin.site.register(UnKnownMissingPerson)
admin.site.register(KnownMissingPerson)
admin.site.register(UserSeeUnknownMissingPerson)
admin.site.register(UserSeeKnownMissingPerson)
admin.site.register(KnownMissingPersonImages)
