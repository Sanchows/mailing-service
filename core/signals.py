from django.db.models.signals import post_save
from django.dispatch import receiver

from core.models import Mailing

########
# an idea for improving:
# when some tags or codes of Mailing are changed, some custom logic will work
########


# @receiver(m2m_changed, sender=Mailing.codes.through)
# def codes_changed_signal(sender, **kwargs):
#     print(kwargs)
#     instance = kwargs.pop('instance')
#     codes = kwargs.pop('pk_set')
#     if kwargs['action'] == 'post_add':
#         pass


# @receiver(m2m_changed, sender=Mailing.tags.through)
# def tags_changed_signal(sender, **kwargs):
#     instance = kwargs.pop('instance')
#     tags = kwargs.pop('pk_set')
#     if kwargs['action'] == 'post_add':
#         pass
