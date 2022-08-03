from .models import Licencia
from rest_framework import serializers
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MinValueValidator, MaxValueValidator


class LicenciaCreationSerializers(serializers.ModelSerializer):
    id=serializers.PrimaryKeyRelatedField(read_only=True)
    num_licencia = serializers.IntegerField(validators=[
            MaxValueValidator(1000000),
            MinValueValidator(1)
        ])
    matricula = serializers.CharField(max_length=10)
    marca = serializers.CharField(max_length=10, allow_null=True)
    modelo = serializers.CharField(max_length=15, allow_null=True)
    color = serializers.CharField(max_length=15, allow_null=True)


    class Meta:
        model = Licencia
        fields = ['id','num_licencia', 'matricula', 'marca','modelo','color']

    def validate(self, attrs):
        num_licencia_exists = Licencia.objects.filter(num_licencia=attrs['num_licencia']).exists()
        if num_licencia_exists:
            raise serializers.ValidationError(detail='Ya existe esa licencia')

        matricula_exists = Licencia.objects.filter(matricula=attrs['matricula']).exists()
        if matricula_exists:
            raise serializers.ValidationError(detail='Ya existe esa matrícula')

        return super().validate(attrs)

class LicenciaDetailSerializers(serializers.ModelSerializer):
    id=serializers.PrimaryKeyRelatedField(read_only=True)
    num_licencia = serializers.IntegerField(validators=[
            MaxValueValidator(1000000),
            MinValueValidator(1)
        ])
    matricula = serializers.CharField(max_length=10)
    marca = serializers.CharField(max_length=10, allow_null=True)
    modelo = serializers.CharField(max_length=15, allow_null=True)
    color = serializers.CharField(max_length=15, allow_null=True)


    class Meta:
        model = Licencia
        fields = ['id','num_licencia', 'matricula', 'marca','modelo','color']

