from .models import VariosDiarios
from rest_framework import serializers
from django.core.validators import MinValueValidator, MaxValueValidator


class VariosDiariosCreationSerializers(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    cantidad = serializers.FloatField(validators=[
        MaxValueValidator(1000000),
        MinValueValidator(-1000000),
    ],
                                      allow_null=True)
    concepto = serializers.CharField(max_length=30, allow_null=True)

    class Meta:
        model = VariosDiarios
        fields = ['id','cantidad', 'concepto']


class VariosDiariosDetailSerializers(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    cantidad = serializers.FloatField(validators=[
        MaxValueValidator(1000000),
        MinValueValidator(-1000000),
    ],
                                      allow_null=True)
    concepto = serializers.CharField(max_length=50, allow_null=True)

    class Meta:
        model = VariosDiarios
        fields = ['id','cantidad', 'concepto']
