import logging

from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch.dispatcher import receiver
from django.utils import timezone

from cmj4.core.signals_functions import send_signal_for_websocket_time_refresh

logger = logging.getLogger(__name__)


@receiver([post_save, post_delete], dispatch_uid='timerefresh_post_signal')
def timerefresh_post_signal(sender, instance, **kwargs):
    logger.debug(f'START timerefresh_post_signal {timezone.localtime()}')
    send_signal_for_websocket_time_refresh(instance, **kwargs)
    logger.debug(f'END timerefresh_post_signal {timezone.localtime()}')

