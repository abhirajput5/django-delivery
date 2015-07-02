import time
import smtplib
import logging
import socket
from datetime import datetime
from django.db import models
from django.conf import settings
from django.core.mail import EmailMessage, EmailMultiAlternatives
import lockfile

logger = logging.getLogger('django_delivery')
delivery_settings = getattr(settings, 'DJANGO_DELIVERY', {
    'is_active': True,
    'lock_wait_timeout': -1,
})


#===============================================================================
class MessageBase(models.Model):
    to_address = models.CharField(max_length=50)
    from_address = models.CharField(max_length=50)
    subject = models.CharField(max_length=100)
    text = models.TextField()
    html = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)

    #===========================================================================
    class Meta:
        abstract = True


#===============================================================================
class MessageManager(models.Manager):
    
    #---------------------------------------------------------------------------
    def send_all(self):
        '''
        Send all available messages.
        '''
        if not delivery_settings.get('is_active', True):
            logger.debug('django_delivery inactive')
            return False

        now = datetime.now()
        lock = lockfile.FileLock("send_all")
        try:
            lock.acquire(delivery_settings.get('lock_wait_timeout', -1))
        except lockfile.AlreadyLocked:
            logger.warn('{}: Lock already in place.'.format(now))
            return False
        except lockfile.LockTimeout:
            logger.warn('{}: Waiting for the lock timed out. quitting.'.format(now))
            return False

        errors = sent = 0
        start_time = time.time()
        try:
            for message in self.all():
                now = datetime.now()
                msg = unicode(message).encode("utf-8")

                try:
                    logger.info('Sending message {}'.format(msg))
                    message.send()
                except(socket.error, smtplib.SMTPException) as err:
                    logger.info('Message {} failure: {}'.format(msg, err))
                    MessageLog.objects.log(message, False, unicode(err))
                    errors += 1
                else:
                    MessageLog.objects.log(message)
                    message.delete()
                    sent += 1

        finally:
            lock.release()

        if sent or errors:
            logger.info('[{}] Mailer: {} sent | {} errors ({:.3} seconds)'.format(
                datetime.utcnow(),
                sent,
                errors,
                time.time() - start_time
            ))


    
#===============================================================================
class Message(MessageBase):
    
    objects = MessageManager()
    
    #---------------------------------------------------------------------------
    def send(self):
        alt = bool(self.html)
        MessageClass = EmailMultiAlternatives if alt else EmailMessage
        em = MessageClass(
            self.subject,
            self.text,
            self.from_address,
            [self.to_address],
            headers={'Reply-To': self.from_address}
        )
        
        if alt:
            em.attach_alternative(self.html, 'text/html')
            
        return em.send()
        
    #---------------------------------------------------------------------------
    def __unicode__(self):
        return 'Message %d: "%s" to %s' % (self.id, self.subject, self.to_address)


#===============================================================================
class MessageLogManager(models.Manager):
    
    #---------------------------------------------------------------------------
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


#===============================================================================
class MessageLog(MessageBase):
    attempted = models.DateTimeField(auto_now_add=True)
    is_success = models.BooleanField(default=True)
    log_message = models.TextField(blank=True)

    objects = MessageLogManager()


