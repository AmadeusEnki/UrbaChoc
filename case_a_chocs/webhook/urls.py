from django.urls import path
from . import views
from webhook.RetrieveAPIView import TicketDetailView
from webhook.views import DetailsView, TicketView


urlpatterns = [
    path('webhook/', views.WebhookView.as_view(), name='webhook'),
    path('webhookget/', views.WebhookView.as_view(), name='webhook'),
    path('tickets/<int:id>', TicketDetailView.as_view(), name='ticket-detail'),
    path('details/<int:pk>/', DetailsView.as_view(), name='details'),
    path('ticket/<int:pk>/', TicketView.as_view(), name='ticket'),
]
