import ipaddress

from rest_framework import serializers

from registry.models import BlockRequest
from .models import Registry


class RegistrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Registry
        fields = ('id', 'ip', 'description')
        read_only_fields = ('id',)

    def validate_ip(self, value):
        try:
            ipaddress.ip_address(value)
        except ValueError:
            raise serializers.ValidationError("Not valid IP address.")
        return value


class BlockRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlockRequest
        fields = ('id', 'user_ip', 'description', 'site')
        read_only_fields = ('id', 'user_ip')
