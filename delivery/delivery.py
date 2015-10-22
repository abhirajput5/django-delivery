import re
import time

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.utils.encoding import force_unicode
from django.template import loader
from django.core.mail import send_mail as core_send_mail

from .models import Message

NICE_EMAIL_FMT = '"{}" <{}>'

recipient_string_splitter = re.compile(r'[\s,;:]+', re.M).split

#-------------------------------------------------------------------------------
def nice_email(email, name=''):
    return NICE_EMAIL_FMT.format(name, email) if name else email


TO_MANAGERS = [nice_email(em, name) for name, em in settings.MANAGERS]
TO_ADMINS   = [nice_email(em, name) for name, em in settings.ADMINS]


#-------------------------------------------------------------------------------
def nice_user_email(u):
    return nice_email(u.email, u.get_full_name() or u.username)


#-------------------------------------------------------------------------------
def normalize_recipients(recipients):
    recipients = recipients or TO_ADMINS
    if isinstance(recipients, basestring):
        return [s.strip() for s in recipient_string_splitter(recipients)]

    return [
        nice_user_email(item) if isinstance(item, User) else item 
        for item in recipients
    ]


#-------------------------------------------------------------------------------
def send_mail(
    subject,
    message,
    from_email=None,
    recipient_list=None,
    html=''
):
    from_email = from_email or settings.DEFAULT_FROM_EMAIL
    subject = force_unicode(subject)
    for to_address in normalize_recipients(recipient_list):
        Message.objects.create(
            to_address=to_address,
            from_address=from_email,
            subject=subject,
            text=message,
            html=html
        )


#-------------------------------------------------------------------------------
def mail_admins(subject, message, html=''):
    subject = settings.EMAIL_SUBJECT_PREFIX + force_unicode(subject)
    send_mail(subject, message, recipient_list=TO_ADMINS, html=html)


#-------------------------------------------------------------------------------
def mail_managers(subject, message, html=''):
    subject = settings.EMAIL_SUBJECT_PREFIX + force_unicode(subject)
    send_mail(subject, message, recipient_list=TO_MANAGERS, html=html)


#-------------------------------------------------------------------------------
def mail_user(user, subject, message, html='', fail_silently=False):
    addr = [nice_user_email(user)]
    return send_mail(subject, message, recipient_list=addr, html=html)


#-------------------------------------------------------------------------------
def render_message(template, data=None, request=None):
    '''
    Render the body of the email as a template. 
    '''
    data = data or {}
    if 'site' not in data:
        data['site'] = Site.objects.get_current()
    
    return loader.render_to_string(template, data, request=request)
