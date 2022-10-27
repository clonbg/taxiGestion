from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from . import serializers
from .models import Reserva

class HelloReservasView(generics.GenericAPIView):
    def get(self, request):
        return Response(data={"message": "Hola reserva"}, status=status.HTTP_200_OK)

class ReservaCreateListView(generics.GenericAPIView):
    serializer_class=serializers.ReservaCreationSerializer
    queryset=Reserva.objects.all()
    def get(self,request):
        serializer = self.serializer_class(instance=self.queryset.all(), many=True)
        return Response(data=serializer.data,status=status.HTTP_200_OK)

    def post(self,request):
        pass

class ReservaDetailView(generics.GenericAPIView):

    def get(self,request,reserva_id):
        pass

    def put(self,request,reserva_id):
        pass


