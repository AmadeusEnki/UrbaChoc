from rest_framework import serializers
from .models import Ticket, Session, Location, Price, Buyer, Details

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['name', 'street', 'city', 'postcode']

class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ['name', 'date', 'time', 'doors', 'location']

class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = ['amount', 'currency']

class BuyerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Buyer
        fields = ['role', 'firstName', 'lastName', 'email', 'postcode']

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['number', 'type', 'title', 'category', 'event', 'eventId', 
                  'cancellationReason', 'sessions', 'promoter', 'price']

class DetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Details
        fields = ['ticket', 'buyer', 'event']
