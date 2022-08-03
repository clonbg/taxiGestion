from .models import IngresoDiario
from rest_framework import serializers
from django.core.validators import MinValueValidator, MaxValueValidator
from taxistas.models import User
from taxistas.serializers import UserCreationSerializers


class IngresoDiarioCreationSerializers(serializers.ModelSerializer):
    id=serializers.PrimaryKeyRelatedField(read_only=True)
    dia = serializers.DateField()
    imagen = serializers.ImageField(allow_null=True)
    total_efectivo = serializers.FloatField(validators=[
        MaxValueValidator(1000000),
        MinValueValidator(1)
    ],allow_null=True)
    total_apps = serializers.FloatField(validators=[
        MaxValueValidator(1000000),
        MinValueValidator(1)
    ],allow_null=True)
    total_tpv = serializers.FloatField(validators=[
        MaxValueValidator(1000000),
        MinValueValidator(1)
    ],allow_null=True)
    varios = serializers.FloatField(validators=[
        MaxValueValidator(1000000),
        MinValueValidator(-1000000)
    ],allow_null=True)
    taxista = UserCreationSerializers(read_only=True)
    taxista_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=User.objects.all(), source='taxista')


    class Meta:
        model = IngresoDiario
        fields = ['id','dia','imagen','total_efectivo','total_apps','total_tpv','varios','taxista','taxista_id']

    def validate(self, attrs):
        ingresos_diarios_taxista = IngresoDiario.objects.filter(dia=attrs['dia'],taxista_id=attrs['taxista']).exists()
        if ingresos_diarios_taxista:
            raise serializers.ValidationError(detail='Ya tienes ese día')
        return super().validate(attrs)

