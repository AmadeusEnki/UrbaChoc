import json
from pulsar import Client
import logging

# Configuration du logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration du client Pulsar
try:
    client = Client('pulsar://localhost:6650')
    logger.info("Client Pulsar créé avec succès.")
except Exception as e:
    logger.error(f"Erreur lors de la création du client Pulsar: {e}")

# Configuration du producteur Pulsar
try:
    topic = 'persistent://public/default/my_topic1'
    producer = client.create_producer(topic)
    logger.info("Producteur Pulsar créé pour le topic.")
except Exception as e:
    logger.error(f"Erreur lors de la création du producteur Pulsar: {e}")

def publish_to_pulsar(data):
    try:
        # Préparation du message
        data_json = json.dumps(data)
        message = data_json.encode('utf-8')

        # Envoi du message
        producer.send(message)
        logger.info("Message envoyé avec succès à Pulsar.")
    except Exception as e:
        logger.error(f"Erreur lors de l'envoi du message à Pulsar: {e}")
