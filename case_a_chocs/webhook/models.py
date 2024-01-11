from django.core.validators import RegexValidator
from django.db import models
    
class Session(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField(null=True, blank=True)
    doors = models.TimeField(null=True, blank=True)
    location = models.ForeignKey('Location', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} on {self.date}"

class Location(models.Model):
    name = models.CharField(max_length=200)
    street = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    postcode = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.name}, {self.city}"

class Price(models.Model):
    amount = models.CharField(max_length=10, validators=[RegexValidator(regex="^\d+\.\d{2}$")])
    currency = models.CharField(max_length=3, validators=[RegexValidator(regex="^[A-Z]{3}$")])

    def __str__(self):
        return f"{self.amount} {self.currency}"

class Ticket(models.Model):
    TICKET_TYPE_CHOICES = [
        ('online_presale', 'Online Presale'),
        ('ticket_proof', 'Ticket Proof'),
        ('self_ticket', 'Self Ticket'),
    ]

    CANCELLATION_REASON_CHOICES = [
        ('', 'None'),
        ('undef_cancellation', 'Undefined Cancellation'),
        ('order_mistake', 'Order Mistake'),
        ('event_cancellation', 'Event Cancellation'),
        ('event_postponed', 'Event Postponed'),
        ('stolen', 'Stolen'),
        ('test_ticket', 'Test Ticket'),
        ('selfticket_mistake', 'Selfticket Mistake'),
    ]

    number = models.CharField(max_length=50, unique=True)
    type = models.CharField(max_length=20, choices=TICKET_TYPE_CHOICES)
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    event = models.CharField(max_length=200)
    eventId = models.IntegerField()
    cancellationReason = models.CharField(max_length=50, choices=CANCELLATION_REASON_CHOICES, blank=True, default='')
    sessions = models.ManyToManyField(Session)
    promoter = models.CharField(max_length=200)
    price = models.ForeignKey(Price, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} - {self.number}"

class Buyer(models.Model):
    BUYER_ROLE_CHOICES = [
        ('customer', 'Customer'),
        ('self_ticket', 'Self Ticket'),
        ('point_of_sale', 'Point of Sale'),
        ('unknown', 'Unknown'),
    ]

    role = models.CharField(max_length=20, choices=BUYER_ROLE_CHOICES)
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True)
    postcode = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.firstName} {self.lastName} - {self.role}"

class Details(models.Model):
    EVENT_CHOICES = [
        ('ticket_created', 'Ticket Created'),
        ('ticket_updated', 'Ticket Updated'),
    ]
    ticket = models.OneToOneField(Ticket, on_delete=models.CASCADE)
    buyer = models.OneToOneField(Buyer, on_delete=models.CASCADE)
    event = models.CharField(max_length=20, choices=EVENT_CHOICES)

    def __str__(self):
        return f"{self.ticket} - {self.event}"