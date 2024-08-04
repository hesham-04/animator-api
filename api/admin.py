from django.contrib import admin
from .models import Media


class MediaAdmin(admin.ModelAdmin):
    list_display = ('id', 'driving_video', 'input_image', 'output_video', 'created_at')
    search_fields = ('id',)
    list_filter = ('created_at',)
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)

    # Optionally, customize how fields are displayed in the form
    fieldsets = (
        (None, {
            'fields': ('driving_video', 'input_image', 'output_video')
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',),
        }),
    )


admin.site.register(Media, MediaAdmin)
