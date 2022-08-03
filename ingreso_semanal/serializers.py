from .models import IngresoSemanal
from rest_framework import serializers
from django.core.validators import MinValueValidator, MaxValueValidator
from taxistas.models import User
from taxistas.serializers import UserCreationSerializers
from datetime import datetime, timedelta


class IngresoSemanalCreationSerializers(serializers.ModelSerializer):
    id=serializers.PrimaryKeyRelatedField(read_only=True)
    dia_inicio = serializers.DateField()#unique
    dia_fin = serializers.DateField()#unique
    imagen_semana = serializers.ImageField(allow_null=True)
    total_efectivo_semana = serializers.FloatField(validators=[
        MaxValueValidator(1000000),
        MinValueValidator(1)
    ],allow_null=True)
    total_apps_semana = serializers.FloatField(validators=[
        MaxValueValidator(1000000),
        MinValueValidator(1)
    ],allow_null=True)
    total_tpv_semana = serializers.FloatField(validators=[
        MaxValueValidator(1000000),
        MinValueValidator(1)
    ],allow_null=True)
    varios_semana = serializers.FloatField(validators=[
        MaxValueValidator(1000000),
        MinValueValidator(-1000000)
    ],allow_null=True)
    taxista = UserCreationSerializers(read_only=True)
    taxista_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=User.objects.all(), source='taxista')

    class Meta:
        model = IngresoSemanal
        fields = ['id','dia_inicio','dia_fin','imagen_semana','total_efectivo_semana','total_apps_semana','total_tpv_semana','varios_semana','taxista','taxista_id']

    def validate(self, attrs):
        es_menor_o_igual = attrs['dia_inicio']<=attrs['dia_fin']
        # No tiene ninguno de los días ya apuntados
        dias=attrs['dia_inicio']-attrs['dia_fin']
        raise serializers.ValidationError(detail=attrs['dia_inicio']-attrs['dia_fin'])
        return super().validate(attrs)

