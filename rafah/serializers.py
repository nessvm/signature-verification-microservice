from rest_framework import serializers

from jericho.models import Signature

__author__ = 'Nestor Velazquez'


class SignatureSerializer(serializers.HyperlinkedModelSerializer):
    given_name = serializers.CharField(max_length=64, write_only=True)
    paternal_name = serializers.CharField(max_length=64, write_only=True)
    maternal_name = serializers.CharField(max_length=64, write_only=True)
    birth_date = serializers.DateField(write_only=True)
    paternal_maternal_name = serializers.CharField(
        max_length=64, write_only=True
    )
    loan_amount = serializers.CharField(max_length=64, write_only=True)
    request_date = serializers.DateField(write_only=True)

    pk = serializers.UUIDField(read_only=True)
    contract_number = serializers.CharField(max_length=64)
    created = serializers.DateField(read_only=True)
    mac = serializers.CharField(read_only=True)

    def create(self, validated_data):
        return self.Meta.model.objects.create_signature(**validated_data)

    class Meta:
        model = Signature
