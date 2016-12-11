from rest_framework import serializers
from .models import User

class UserSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    booking_order = serializers.ListField(
        child=serializers.CharField())
    transaction_total = serializers.DecimalField(max_digits=8, decimal_places= 2)
