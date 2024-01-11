from django.contrib import admin
from .models import Ticket, Session, Location, Price, Buyer, Details

admin.site.register(Ticket)
admin.site.register(Session)
admin.site.register(Location)
admin.site.register(Price)
admin.site.register(Buyer)
admin.site.register(Details)
