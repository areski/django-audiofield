from django.contrib import admin
from django.db.models import *
from audiofield.models import AudioFile
from django.conf import settings
from django.utils.translation import ugettext as _
import os


class AudioFileAdmin(admin.ModelAdmin):
    """Allows the administrator to view and modify uploaded audio files"""
    list_display = ('id', 'name', 'audio_file_player', 'user')
    #list_display_links = ['id', 'name',]
    ordering = ('id', )

    actions = ['custom_delete_selected']

    def custom_delete_selected(self, request, queryset):
        #custom delete code
        n = queryset.count()
        for i in queryset:
            if i.audio_file:
                if os.path.exists(i.audio_file.path):
                    os.remove(i.audio_file.path)
            i.delete()
        self.message_user(request, _("Successfully deleted %d audio files.") % n)
    custom_delete_selected.short_description = "Delete selected items"

    def get_actions(self, request):
        actions = super(AudioFileAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

admin.site.register(AudioFile, AudioFileAdmin)
