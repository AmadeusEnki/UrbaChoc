import hmac
import logging
import hashlib
import datetime
from retrying import retry
from rest_framework import status
from django.db import transaction
from rest_framework.views import APIView
from .serializers import TicketSerializer, BuyerSerializer, DetailsSerializer, PriceSerializer, SessionSerializer, LocationSerializer
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from case_a_chocs.config import PETZI_SECRET_KEY
from rest_framework.decorators import parser_classes
from .models import Ticket, Buyer, Details, Price, Session, Location
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated


logger = logging.getLogger(__name__)

class WebhookView(APIView):
    @parser_classes([JSONParser])
    @retry(wait_fixed=1000, stop_max_attempt_number=3)
    def post(self, request, *args, **kwargs):
        signature_header = request.headers.get('Petzi-Signature')
        if not self.is_valid_signature(request.body, signature_header):
            return self.log_and_respond('Signature invalide')

        data = JSONParser().parse(request)
        print("Données reçues :", data)
        event_type = data.get('event')
        ticket_details = data.get('details')

        if event_type not in ['ticket_created', 'ticket_updated']:
            return self.log_and_respond('Type d\'événement non pris en charge')

        if not ticket_details:
            return self.log_and_respond('Données du ticket manquantes')

        try:
            with transaction.atomic():
                if event_type == 'ticket_created':
                    self.handle_ticket_created(ticket_details, event_type)
                elif event_type == 'ticket_updated':
                    self.handle_ticket_updated(ticket_details)

        except Exception as e:
            logger.error(f"Erreur lors du traitement : {e}")
            return Response({'message': f'Erreur lors du traitement : {e}'}, status=200)

        return Response({'message': 'Traitement réussi'}, status=200)

    def is_valid_signature(self, body, signature_header):
        print("Signature Header:", signature_header)
        # Étape 1 : Extraction de la signature et du timestamp
        signature_parts = dict(part.split("=") for part in signature_header.split(","))
        
        # Étape 2 : Préparation de la chaîne à signer
        body_to_sign = f"{signature_parts['t']}.{body.decode()}"
        
        # Étape 3 : Calcul de la signature attendue
        secret = PETZI_SECRET_KEY.encode()
        expected_signature = hmac.new(secret, body_to_sign.encode(), hashlib.sha256).hexdigest()

        # Étape 4 : Comparaison des signatures
        if not hmac.compare_digest(expected_signature, signature_parts['v1']):
            return False
        
        # Étape 5 : Rejet des messages trop anciens
        message_time = datetime.datetime.fromtimestamp(int(signature_parts['t']))
        time_delta = datetime.datetime.utcnow() - message_time
        return time_delta.total_seconds() < 300  # Exemple : 5 minutes de tolérance
    
    def handle_ticket_created(self, details, event_type):
        with transaction.atomic():

            # Valider et créer le Price
            price_info = details.get('ticket').get('price')
            price_serializer = PriceSerializer(data=price_info)
            if price_serializer.is_valid(raise_exception=True):
                price = price_serializer.save()
            

            # Valider et créer les Sessions et leurs Locations
            sessions_info = details.get('ticket').get('sessions', [])
            session_ids = []  # Liste pour stocker les IDs des sessions créées
            for session_info in sessions_info:
                location_info = session_info.pop('location', None)
                if location_info:
                    location_serializer = LocationSerializer(data=location_info)
                    if location_serializer.is_valid(raise_exception=True):
                        location = location_serializer.save()
                    session_info['location'] = location.id

                session_serializer = SessionSerializer(data=session_info)
                if session_serializer.is_valid(raise_exception=True):
                    session = session_serializer.save()
                    session_ids.append(session.id)
                

           # Préparer les données du Ticket en incluant l'ID de Price
            ticket_data = details.get('ticket')
            ticket_data['price'] = price.id
            ticket_data['sessions'] = session_ids
            ticket_serializer = TicketSerializer(data=ticket_data)
            if ticket_serializer.is_valid(raise_exception=True):
                ticket = ticket_serializer.save()
            

            # Validez et créez le Buyer
            buyer_serializer = BuyerSerializer(data=details.get('buyer'))
            if buyer_serializer.is_valid(raise_exception=True):
                buyer = buyer_serializer.save()            

            # Créez les Details
            details_data = {'ticket': ticket.id, 'buyer': buyer.id, 'event': 'ticket_created'}
            details_serializer = DetailsSerializer(data=details_data)
            if details_serializer.is_valid(raise_exception=True):
                details_serializer.save() 

    def handle_ticket_updated(self, details):
        with transaction.atomic():
            ticket_number = details.get('ticket').get('number')

            # Vérifier si le ticket existe
            try:
                ticket = Ticket.objects.get(number=ticket_number)
            except Ticket.DoesNotExist:
                raise ValueError("Ticket non trouvé.")

            # Logique du ticket_updated

    
    def log_and_respond(self, message):
        logger.warning(message)
        return Response({'message': message}, status=200)
    
    
class DetailsView(RetrieveAPIView):
    queryset = Details.objects.all()
    serializer_class = DetailsSerializer
    permission_classes = (IsAuthenticated,)
 
class TicketView(RetrieveAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = (IsAuthenticated,)
