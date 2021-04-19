from django.contrib import admin
from .models import (
    UnKnownMissingPerson,
    KnownMissingPerson,
    UserSeeknownMissingPerson,
    UserSeeUnknownMissingPerson,
    KnownMissingPersonImages,
)

admin.site.register(UnKnownMissingPerson)
admin.site.register(KnownMissingPerson)
admin.site.register(UserSeeUnknownMissingPerson)
admin.site.register(UserSeeknownMissingPerson)
admin.site.register(KnownMissingPersonImages)
