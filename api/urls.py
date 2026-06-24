from django.urls import path
from tracker import views

urlpatterns = [
    path('mpesa/webhook/', views.MPesaWebhookView.as_view(), name='mpesa_webhook'),
]
