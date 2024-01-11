from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Ticket, Details
from .pulsar_client import publish_to_pulsar
import logging

# Configuration du logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@receiver(post_save, sender=Details)
def publish_new_ticket_to_pulsar(sender, instance, created, **kwargs):
    if created:
        logger.info("Nouveau ticket créé, préparation de la publication à Pulsar.")

        # Récupération de l'instance de Ticket
        ticket_instance = instance.ticket

        # Préparation des données à publier
        data_to_publish = {
            'id': ticket_instance.id,
            'event': instance.event,
        }

        # Publication à Pulsar
        publish_to_pulsar(data_to_publish)
        logger.info("Données publiées à Pulsar.")
