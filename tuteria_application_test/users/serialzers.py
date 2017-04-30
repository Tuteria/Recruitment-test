from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    booking_order = serializers.SerializerMethodField()
    transaction_total = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name',
                  'booking_order', 'transaction_total']

    @staticmethod
    def get_booking_order(param):
        return [booking.order for booking in param.orders.all()]

    @staticmethod
    def get_transaction_total(param):
        return param.transaction_total
