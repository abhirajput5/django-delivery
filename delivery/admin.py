from django.contrib import admin
from .models import (Message, MessageLog)

#===============================================================================
class MessageAdmin(admin.ModelAdmin):
    list_display = ( 
        'id',
        'to_address',
        'from_address',
        'subject',
        'text',
        'html',
        'created',
    )


#===============================================================================
class MessageLogAdmin(admin.ModelAdmin):
    list_display = ( 
        'id',
        'to_address',
        'from_address',
        'subject',
        'text',
        'html',
        'created',
        'attempted',
        'is_success',
        'log_message',
    )


admin.site.register(Message, MessageAdmin)
admin.site.register(MessageLog, MessageLogAdmin)