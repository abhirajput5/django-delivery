from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import (Message, MessageLog, delivery_settings)


#===============================================================================
class MessageAdmin(admin.ModelAdmin):
    list_display = ( 
        'id',
        'to_address',
        'from_address',
        'subject',
        'created',
    )
    
    readonly_fields = (
        'to_address',
        'from_address',
        'subject',
        'created',
        'text_content',
        'html',
    )
    
    fieldsets = (
        (None, {
            'fields': (
                'from_address',
                'to_address',
                'subject',
                'created',
            )
        }),
        ('Message Content', {
            'fields': (
                'text_content',
                'html',
            ),
            'classes': ('pre',)
        }),
    )
    
    #---------------------------------------------------------------------------
    def pre_field(self, text):
        return mark_safe('\n<pre>{}</pre>'.format(text))
        
    #---------------------------------------------------------------------------
    def text_content(self, instance):
        return self.pre_field(instance.text)


#===============================================================================
class MessageLogAdmin(MessageAdmin):
    list_display = MessageAdmin.list_display + (
        'attempted',
        'is_success',
    )
    fieldsets = MessageAdmin.fieldsets + (
        ('Message Results', {
            'fields': (
                ('is_success', 'attempted'),
                'log_message_content'
            ),
            'classes': ('pre',)
        }),
    )
    readonly_fields = MessageAdmin.readonly_fields + (
        'attempted',
        'is_success',
        'log_message_content',
    )

    #---------------------------------------------------------------------------
    def log_message_content(self, instance):
        return self.pre_field(instance.log_message)


if delivery_settings.get('show_message_admin'):
    admin.site.register(Message, MessageAdmin)
admin.site.register(MessageLog, MessageLogAdmin)
