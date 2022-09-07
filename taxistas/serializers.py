from .models import User
from rest_framework import serializers
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MinValueValidator, MaxValueValidator
from licencias.models import Licencia
from licencias.serializers import LicenciaCreationSerializers


class UserCreationSerializers(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    dni = serializers.CharField(max_length=25)
    nombre = serializers.CharField(max_length=20)
    apellidos = serializers.CharField(max_length=50)
    sueldo = serializers.IntegerField(
        validators=[MaxValueValidator(100),
                    MinValueValidator(0)])
    foto = serializers.ImageField(allow_null=True)
    licencia = LicenciaCreationSerializers(read_only=True)
    licencia_id = serializers.PrimaryKeyRelatedField(


        write_only =True,
        queryset=Licencia.objects.all(),
        source='licencia',
        allow_null=True)
    email = serializers.EmailField(max_length=80)
    phone_number = serializers.CharField()
    password = serializers.CharField(
        min_length=4)
    is_superuser = serializers.BooleanField(allow_null=True, read_only=True)
    is_staff = serializers.BooleanField(allow_null=True, read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'dni', 'nombre', 'apellidos', 'sueldo', 'foto', 'licencia',
            'licencia_id', 'email', 'phone_number', 'password',
            'is_superuser','is_staff'
        ]

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        user.set_password('')
        return user

    def validate(self, attrs):
        dni_exists = User.objects.filter(dni=attrs['dni']).exists()
        if dni_exists:
            raise serializers.ValidationError(detail='Ya existe ese dni')

        email_exists = User.objects.filter(email=attrs['email']).exists()
        if email_exists:
            raise serializers.ValidationError(detail='Ya existe ese email')

        return super().validate(attrs)


class UserDetailSerializers(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    dni = serializers.CharField(max_length=25)
    nombre = serializers.CharField(max_length=20)
    apellidos = serializers.CharField(max_length=50)
    sueldo = serializers.IntegerField(
        validators=[MaxValueValidator(100),
                    MinValueValidator(0)])
    foto = serializers.ImageField(allow_null=True, required=False)
    licencia = LicenciaCreationSerializers(read_only=True,)
    licencia_id = serializers.PrimaryKeyRelatedField(
        write_only=True,
        queryset=Licencia.objects.all(),
        source='licencia',
        allow_null=True,
        required=False)
    email = serializers.EmailField(max_length=80)
    phone_number = serializers.CharField()
    password = serializers.CharField(allow_null=True, read_only=True)
    is_superuser = serializers.BooleanField(allow_null=True, read_only=True)
    is_staff = serializers.BooleanField(allow_null=True, read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'dni', 'nombre', 'apellidos', 'sueldo', 'foto', 'licencia',
            'licencia_id', 'email', 'phone_number', 'password',
            'is_superuser', 'is_staff'
        ]

    def update(self, instance, validated_data):
        updated_user = super().update(instance, validated_data)
        updated_user.save()
        updated_user.set_password('')
        return updated_user
