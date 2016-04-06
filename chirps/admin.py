from chirps.models import Chirp, Tag
from django.contrib import admin


@admin.register(Chirp)
class ChirpAdmin(admin.ModelAdmin):
    # This is all that is really needed to be useful.  Django figures out
    # what needs to happen on the detail page
    list_display = ('id', 'subject', 'user', 'created_at', 'modified_at')

    # This will simply add the read only fields to page to be displayed
    readonly_fields = ('created_at', 'modified_at')

    # Much more complicated layouts
    fieldsets = (
        (None, {
            "fields": ("subject", "message", "image", 'user')
        }),
        ('Read Only Fields', {
            'classes': ("collapse", ),
            'fields': ('created_at', 'modified_at')
        })
    )

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
