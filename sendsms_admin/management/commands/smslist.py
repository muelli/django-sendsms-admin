#!/usr/bin/env python
from datetime import datetime
from json import JSONEncoder
from optparse import make_option

from django.core.management.base import BaseCommand, CommandError

from sendsms_admin.models import SmsMessage

class MessageEncoder(JSONEncoder):
    '''A simple class to JSON encode a SmsMessage'''

    def default(self, obj):
        if isinstance(obj, SmsMessage):
            return {'id': obj.id,
                    'from': obj.from_phone,
                    'to': obj.to_phones,
                    'body': obj.body,
                    'flash': obj.flash,
                    'sent_at': obj.sent_at,}
        elif isinstance(obj, datetime):
            return obj.isoformat()
        else:
            return JSONEncoder.default(self, obj)

class Command(BaseCommand):
    args = "[id ...]"
    help = "Lists saved SMS"
    
    option_list = BaseCommand.option_list + (
        make_option('--format',
            dest='format',
            default='json',
            help='Select format for output. Options: JSON'),
        make_option('--not-sent',
            action="store_true",
            dest='not_sent',
            default=False,
            help='Only print SMS with an empty sent_at field'),
        )

    def handle(self, *args, **kwargs):
        verbosity = int(kwargs.pop('verbosity', 1))
        format = kwargs.pop('format', 'json')
        not_sent = kwargs.pop('not_sent', False)

        if args:
            messages = SmsMessage.objects.filter(id__in=args)
        else:
            messages = SmsMessage.objects.all()

        if not_sent:
            messages = messages.filter(sent_at=None)

        if verbosity > 1:
            self.stderr.write('Trying to print {} message(s): {}'.format(
                len(args), args))

        written = 0
        for message in messages:
            serialisation = MessageEncoder().encode(message)
            self.stdout.write(serialisation)
            written += 1

        if written < 1 and verbosity > 0:
                self.stderr.write("No messages to print")
        
        if verbosity > 1:
            self.stderr.write("Finished writing {} messages".format(
                written))
