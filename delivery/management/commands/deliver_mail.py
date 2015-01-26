from django.conf import settings
from django.core.management.base import NoArgsCommand
from delivery.models import Message

#===============================================================================
class Command(NoArgsCommand):
    help = 'Deliver the mail.'
    
    #---------------------------------------------------------------------------
    def handle_noargs(self, **options):
        Message.objects.send_all()
