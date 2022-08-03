from .models import ingresoDiario
from rest_framework import serializers
from django.core.validators import MinValueValidator, MaxValueValidator
from taxistas.models import User
from taxistas.serializers import UserCreationSerializers


class ingresoDiarioCreationSerializers(serializers.ModelSerializer):
    id=serializers.PrimaryKeyRelatedField(read_only=True)
    dia = serializers.DateField()#Unique
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
    taxista_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=User.objects.all(), source='taxista',allow_null=True)


    class Meta:
        model = User
        fields = ['id','dia','imagen','total_efectivo','total_apps','total_tpv','varios','taxista','taxista_id']

    def validate(self, attrs):
        dia_exists = ingresoDiario.objects.filter(dia=attrs['dia']).exists()
        if dia_exists:
            raise serializers.ValidationError(detail='Ya existe ese día')

        return super().validate(attrs)

