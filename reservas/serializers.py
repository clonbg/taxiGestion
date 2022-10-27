from .models import Reserva
from rest_framework import serializers
from taxistas.serializers import UserCreationSerializers
from django.utils.timezone import now
from taxistas.models import User


class ReservaCreationSerializer(serializers.ModelSerializer):
	id = serializers.PrimaryKeyRelatedField(read_only=True)
	nombre = serializers.CharField(max_length=150)
	email = serializers.EmailField(max_length=800)
	direccion = serializers.CharField(max_length=250)
	hora_recogida = serializers.TimeField()
	telefono = serializers.IntegerField()
	taxista = UserCreationSerializers(read_only=True)
	taxista_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=User.objects.all(), source='taxista',allow_null=True)
	confirmada = serializers.BooleanField(default=False)
	hora_creada_reserva = serializers.TimeField(default=now)

	class Meta:
		model=Reserva
		fields=['id','nombre','email','direccion','hora_recogida','telefono','taxista','taxista_id','confirmada','hora_creada_reserva']
