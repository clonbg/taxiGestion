from .models import IngresoDiario
from rest_framework import serializers
from django.core.validators import MinValueValidator, MaxValueValidator
from taxistas.models import User
from taxistas.serializers import UserCreationSerializers


class IngresoDiarioCreationSerializers(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    dia = serializers.DateField()
    imagen = serializers.ImageField(allow_null=True)
    total_efectivo = serializers.FloatField(validators=[
        MaxValueValidator(1000000),
        MinValueValidator(1)
    ], allow_null=True)
    total_apps = serializers.FloatField(validators=[
        MaxValueValidator(1000000),
        MinValueValidator(1)
    ], allow_null=True)
    total_tpv = serializers.FloatField(validators=[
        MaxValueValidator(1000000),
        MinValueValidator(1)
    ], allow_null=True)
    vario = serializers.ListField(
        child=serializers.CharField(allow_null=True, required=False), allow_null=True, required=False)
    taxista = UserCreationSerializers(read_only=True)
    taxista_id = serializers.PrimaryKeyRelatedField(
        write_only=True, queryset=User.objects.all(), source='taxista')

    class Meta:
        model = IngresoDiario
        #fields = ['id','dia','imagen','total_efectivo','total_apps','total_tpv','vario_diario_id','taxista','taxista_id']
        fields = '__all__'

    def validate(self, attrs):
        ingresos_diarios_taxista = IngresoDiario.objects.values_list(
            'dia', 'taxista_id').filter(dia=attrs['dia'], taxista_id=attrs['taxista']).exists()
        if ingresos_diarios_taxista:
            raise serializers.ValidationError(detail='Ya tienes ese día')
        return super().validate(attrs)


class IngresoDiarioDetailSerializers(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    dia = serializers.DateField(read_only=True)
    imagen = serializers.ImageField(required=False,allow_null=True)
    total_efectivo = serializers.FloatField(validators=[
        MaxValueValidator(1000000),
        MinValueValidator(1)
    ], allow_null=True)
    total_apps = serializers.FloatField(validators=[
        MaxValueValidator(1000000),
        MinValueValidator(1)
    ], allow_null=True)
    total_tpv = serializers.FloatField(validators=[
        MaxValueValidator(1000000),
        MinValueValidator(1)
    ], allow_null=True)
    vario = serializers.ListField(
        child=serializers.CharField(allow_null=True, required=False), allow_null=True, required=False)

    taxista = UserCreationSerializers(read_only=True)
    taxista_id = serializers.PrimaryKeyRelatedField(
        write_only=True, queryset=User.objects.all(), source='taxista')

    class Meta:
        model = IngresoDiario
        fields = '__all__'

    def update(self, instance, validated_data):
        print(instance.imagen)
        if instance.imagen:
            print('Existe')
        else:
            print('No existe')
        print(self.data['imagen'])
        print(validated_data['imagen'])
        validated_data['imagen']='jjjjjj'
        # Si existe validated_data[imagen] se guarda la nueva, si no, se queda la vieja
        updated_user = super().update(instance, validated_data)
        print(updated_user)
        updated_user.save()
        return updated_user