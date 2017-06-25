"""Serializers for API."""

from django.db.models import Sum

from rest_framework import serializers

from .models import User, Booking

class UserSerializer(serializers.ModelSerializer):
    """Serializer for the User model."""

    booking_order = serializers.SerializerMethodField()
    transaction_total = serializers.SerializerMethodField()

    def get_booking_order(self, user):
        return [order.order for order in user.orders.all()]

    def get_transaction_total(self, user):
        total = user.wallet.transactions.aggregate(total=Sum('total'))
        
        return str(total['total'])

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'booking_order', 'transaction_total'
            )