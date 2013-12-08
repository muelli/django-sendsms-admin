#-*- coding: utf-8 -*-
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext as _

@python_2_unicode_compatible
class SmsMessage(models.Model):
    from_phone = models.CharField(max_length=255, blank=True, default='')
    to_phones = models.TextField(blank=True, default='', help_text=_('"," seperated list of phone numbers'))
    body = models.TextField(blank=True, default='')
    flash = models.BooleanField(default=False)

    sent_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    
    def __str__(self):
        return u"Message (from: {}; To: {}): {}".format(
            self.from_phone, self.to_phones, self.body)

