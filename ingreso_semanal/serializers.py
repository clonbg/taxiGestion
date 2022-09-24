from .models import IngresoSemanal
from rest_framework import serializers
from django.core.validators import MinValueValidator, MaxValueValidator
from taxistas.models import User
from taxistas.serializers import UserCreationSerializers
from datetime import datetime, timedelta


class IngresoSemanalCreationSerializers(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    dia_inicio = serializers.DateField()  # unique
    dia_fin = serializers.DateField()  # unique
    imagen_semana = serializers.ImageField(allow_null=True)
    total_efectivo_semana = serializers.FloatField(validators=[
        MaxValueValidator(1000000)], allow_null=True)
    total_apps_semana = serializers.FloatField(validators=[
        MaxValueValidator(1000000)
    ], allow_null=True)
    total_tpv_semana = serializers.FloatField(validators=[
        MaxValueValidator(1000000)
    ], allow_null=True)
    varios_semana = serializers.FloatField(validators=[
        MaxValueValidator(1000000),
        MinValueValidator(-1000000)
    ], allow_null=True)
    taxista = UserCreationSerializers(read_only=True)
    taxista_id = serializers.PrimaryKeyRelatedField(
        write_only=True, queryset=User.objects.all(), source='taxista')

    class Meta:
        model = IngresoSemanal
        fields = ['id', 'dia_inicio', 'dia_fin', 'imagen_semana', 'total_efectivo_semana',
                  'total_apps_semana', 'total_tpv_semana', 'varios_semana', 'taxista', 'taxista_id']

    # def validate(self, attrs):
    #     # dia_inicio menor que el dia_fin
    #     es_menor_o_igual = attrs['dia_inicio']<=attrs['dia_fin']
    #     if not es_menor_o_igual:
    #         raise serializers.ValidationError(detail='El día de inicio debe ser menor o igual al de finalización')
    #     # No existe ningún dia_fin mayor o igual que el dia_inicio que estamos poniendo
    #     ingresos_semanales_taxista = IngresoSemanal.objects.filter(taxista_id=attrs['taxista'])
    #     ingresos_fechas_erroneas = ingresos_semanales_taxista.values_list('dia_fin').filter(dia_fin__gte=attrs['dia_inicio'])
    #     if ingresos_fechas_erroneas:
    #         raise serializers.ValidationError(detail='Ya existen fechas mayores o iguales que el dia de inicio')
    #     return super().validate(attrs)


class IngresoSemanalDetailSerializers(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    dia_inicio = serializers.DateField()  # unique
    dia_fin = serializers.DateField()  # unique
    imagen_semana = serializers.ImageField(required=False, allow_null=True)
    total_efectivo_semana = serializers.FloatField(validators=[
        MaxValueValidator(1000000)
    ], allow_null=True)
    total_apps_semana = serializers.FloatField(validators=[
        MaxValueValidator(1000000)
    ], allow_null=True)
    total_tpv_semana = serializers.FloatField(validators=[
        MaxValueValidator(1000000)
    ], allow_null=True)
    varios_semana = serializers.FloatField(validators=[
        MaxValueValidator(1000000),
        MinValueValidator(-1000000)
    ], allow_null=True)
    taxista = UserCreationSerializers(read_only=True)
    taxista_id = serializers.PrimaryKeyRelatedField(
        write_only=True, queryset=User.objects.all(), source='taxista')

    class Meta:
        model = IngresoSemanal
        fields = ['id', 'dia_inicio', 'dia_fin', 'imagen_semana', 'total_efectivo_semana',
                  'total_apps_semana', 'total_tpv_semana', 'varios_semana', 'taxista', 'taxista_id']

    # def validate(self, attrs):
    #     # dia_inicio menor que el dia_fin
    #     es_menor_o_igual = attrs['dia_inicio']<=attrs['dia_fin']
    #     if not es_menor_o_igual:
    #         raise serializers.ValidationError(detail='El día de inicio debe ser menor o igual al de finalización')
    #     # No existe ningún dia_fin mayor o igual que el dia_inicio que estamos poniendo, menos el actual
    #     ingresos_semanales_taxista = IngresoSemanal.objects.filter(taxista_id=attrs['taxista'])
    #     ingresos_fechas_erroneas = ingresos_semanales_taxista.filter(dia_fin__gte=attrs['dia_inicio'])
    #     if ingresos_fechas_erroneas.count()!=1:
    #         raise serializers.ValidationError(detail='Las fechas sobreescriben otras fechas')
    #     return super().validate(attrs)
