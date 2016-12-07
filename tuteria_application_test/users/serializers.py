from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    booking_order = serializers.SerializerMethodField()
    transaction_total = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name',
                  'booking_order', 'transaction_total']

    def get_booking_order(self, obj):
        return [x.order for x in obj.orders.all()]

    def get_transaction_total(self, obj):
        return obj.transaction_total
