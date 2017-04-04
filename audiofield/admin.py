#
# django-audiofield License
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright (C) 2011-2014 Star2Billing S.L.
#
# The Initial Developer of the Original Code is
# Arezqui Belaid <info@star2billing.com>
#

from django.contrib import admin
from audiofield.models import AudioFile
from django.utils.translation import ugettext_lazy as _
import os


class AudioFileAdmin(admin.ModelAdmin):
    """Allows the administrator to view and modify uploaded audio files"""

    list_display = ('id', 'name', 'audio_file_player', 'created_date', 'user')
    # list_display_links = ['id', 'name',]
    ordering = ('id', )

    actions = ['custom_delete_selected']

    def custom_delete_selected(self, request, queryset):
        # custom delete code
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
