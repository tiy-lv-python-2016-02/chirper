from chirps.models import Chirp, Tag, Pledge
from django.contrib import admin

class PledgeInline(admin.TabularInline):
    model = Pledge

@admin.register(Chirp)
class ChirpAdmin(admin.ModelAdmin):
    # This is all that is really needed to be useful.  Django figures out
    # what needs to happen on the detail page
    list_display = ('id', 'subject', 'user', 'created_at', 'modified_at')
    actions = ["archive_chirps"]
    date_hierarchy = "created_at"
    list_filter = ["user", "archived"]
    list_per_page = 10
    list_display_links = ("subject",)
    list_select_related = ["user"]
    search_fields = ["subject", "message"]

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

    inlines = [PledgeInline]

    def archive_chirps(self, request, queryset):
        queryset.update(archived=True)
    archive_chirps.short_description = "Archive Chirps"

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
