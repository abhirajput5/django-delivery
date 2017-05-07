import time
import smtplib
import logging
import socket
from datetime import datetime
from django.db import models
from django.conf import settings
from anymail.message import AnymailMessage

logger = logging.getLogger('django_delivery')

delivery_settings = dict({
    'is_active': True,
    'reply_to': True,
    'show_message_admin': True,
}, **getattr(settings, 'DJANGO_DELIVERY', {}))


class MessageBase(models.Model):
    to_address = models.CharField(max_length=100)
    from_address = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    text = models.TextField()
    html = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Message(MessageBase):
    
    def send(self):
        headers = {}
        reply_to = delivery_settings.get('reply_to')
        if reply_to:
            headers['Reply-To'] = self.from_address if reply_to is True else reply_to

        message = AnymailMessage(
            subject=self.subject,
            body=self.text,
            from_email=self.from_address,
            to=[self.to_address],
            headers=headers
        )

        if self.html:
            message.attach_alternative(self.html, "text/html")
            
        message.send()

        status = message.anymail_status
        recipient = status.recipients.get(self.from_address, None)
        log_message = '{}: {} | {}'.format(
            status.message_id or 'NO_ID',
            recipient.status.upper() if recipient else 'UNKNOWN',
            ','.join(status.status)
        )

        is_success = status.status.issubset({'queued', 'sent'})
        MessageLog.objects.log(
            self,
            is_success,
            log_message
        )

        if is_success:
            self.delete()
            
        return is_success

    def __str__(self):
        return 'Message {}: "{}" to {}'.format(self.id, self.subject, self.to_address)


class MessageLogManager(models.Manager):
    
    def log(self, message, is_success=True, log_message=''):
        """
        create a log entry for an attempt to send the given message and
        record the given result and (optionally) a log message
        """
        
        return self.create(
            to_address=message.to_address,
            from_address=message.from_address,
            subject=message.subject,
            text=message.text,
            html=message.html,
            created=message.created,
            is_success=is_success,
            log_message=log_message,
        )


class MessageLog(MessageBase):
    attempted = models.DateTimeField(auto_now_add=True)
    is_success = models.BooleanField(default=True)
    log_message = models.TextField(blank=True)

    objects = MessageLogManager()


