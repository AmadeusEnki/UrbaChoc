from rest_framework import generics
from .models import Ticket
from .serializers import TicketSerializer
from django.http import Http404

class TicketDetailView(generics.RetrieveAPIView):
    serializer_class = TicketSerializer

    def get_queryset(self):
        id = self.kwargs['id']
        tickets = Ticket.objects.filter(id=id)
        if not tickets:
            raise Http404
        return tickets