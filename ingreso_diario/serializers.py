from .models import IngresoDiario
from rest_framework import serializers
from django.core.validators import MinValueValidator, MaxValueValidator
from taxistas.models import User
from varios_diarios.models import VariosDiarios
from taxistas.serializers import UserCreationSerializers
from varios_diarios.serializers import VariosDiariosCreationSerializers


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
    
    vario_diario = VariosDiariosCreationSerializers(many=True, read_only=True)
    vario_diario_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=VariosDiarios.objects.all(), source='vario_diario',many=True)
    taxista = UserCreationSerializers(read_only=True)
    taxista_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=User.objects.all(), source='taxista')


    class Meta:
        model = IngresoDiario
        #fields = ['id','dia','imagen','total_efectivo','total_apps','total_tpv','vario_diario_id','taxista','taxista_id']
        fields = '__all__'

    def validate(self, attrs):
        ingresos_diarios_taxista = IngresoDiario.objects.values_list('dia','taxista_id').filter(dia=attrs['dia'],taxista_id=attrs['taxista']).exists()
        if ingresos_diarios_taxista:
            raise serializers.ValidationError(detail='Ya tienes ese día')
        return super().validate(attrs)

class IngresoDiarioDetailSerializers(serializers.ModelSerializer):
    id=serializers.PrimaryKeyRelatedField(read_only=True)
    dia = serializers.DateField(read_only=True)
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
    varios_diarios = VariosDiariosCreationSerializers(read_only=True)
    varios_diarios_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=VariosDiarios.objects.all(), source='varios_diarios')
    taxista = UserCreationSerializers(read_only=True)
    taxista_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=User.objects.all(), source='taxista')


    class Meta:
        model = IngresoDiario
        fields = ['id','dia','imagen','total_efectivo','total_apps','total_tpv','varios_diarios','varios_diarios_id','taxista','taxista_id']



