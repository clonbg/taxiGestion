from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from . import serializers
from .models import IngresoDiario
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class HelloIngresoDiarioView(generics.GenericAPIView):
    def get(self, request):
        return Response(data={"message":"Hola ingreso diario"}, status=status.HTTP_200_OK)

class IngresoDiarioCreateView(generics.GenericAPIView):
    serializer_class=serializers.IngresoDiarioCreationSerializers
    queryset=IngresoDiario.objects.all()
    #permission_classes=[IsAuthenticated]

    def get(self, request):
        serializer = self.serializer_class(instance=self.queryset.all(), many=True)
        return Response(data=serializer.data,status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data,status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)