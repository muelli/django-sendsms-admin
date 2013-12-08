#!/usr/bin/env python
from datetime import datetime
from optparse import make_option
from json import JSONEncoder

from django.core.management.base import BaseCommand, CommandError

from sendsms_admin.models import SmsMessage

class Command(BaseCommand):
    args = "<ids>"
    help = "Delete SMS from the database"
    
    def handle(self, *args, **kwargs):
        verbosity = int(kwargs.pop('verbosity', 1))
            
        if verbosity > 1:
            self.stdout.write("About to delete {} message(s): {}".format(
                len(args), args))

        deleted = 0
        for message_id in args:
            try:
                message = SmsMessage.objects.get(id=message_id)
            except SmsMessage.DoesNotExist:
                if verbosity > 1:
                    self.stderr.write("Message with ID {} does not exist" \
                        .format(message_id))
            else:
                self.stdout.write("Deleting message %d" % message.id)
                if verbosity > 1:
                    self.stdout.write("Message: {}".format(message))
                message.delete()
                deleted += 1
        self.stdout.write("Finished deleting {} messages".format(deleted))
