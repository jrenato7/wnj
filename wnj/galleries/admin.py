from django.conf import settings
from django.contrib import admin
from django.utils.html import format_html

from .models import Gallery


class GalleryAdmin(admin.ModelAdmin):
    list_display = ['user', 'image_display', 'created_at', 'approved']
    search_fields = ['likes', 'created_at']
    list_filter = ['approved']
    actions = ['change_approved_status']

    def change_approved_status(self, request, queryset):
        for image in queryset:
            image.approved = not image.approved
            image.save()

    def image_display(self, obj):
        url = settings.MEDIA_ROOT
        pic = str(obj.image)
        img = ''.join([url, pic]) if url not in pic else pic
        html = '''<a href="{image}" target="_blank"><img width="45px" 
        src="{image} "></a>'''.format(image=img)
        return format_html(html)


admin.site.register(Gallery, GalleryAdmin)
