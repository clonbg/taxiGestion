from django.shortcuts import render, get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from . import serializers
from .models import IngresoDiario
from rest_framework.permissions import IsAuthenticated


class IngresoDiarioCreateView(generics.GenericAPIView):
    serializer_class = serializers.IngresoDiarioCreationSerializers
    queryset = IngresoDiario.objects.order_by('-id')
    permission_classes=[IsAuthenticated]

    def get(self, request):
        serializer = self.serializer_class(
            instance=self.queryset.all(), many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IngresoDiarioDetailView(generics.GenericAPIView):
    serializer_class = serializers.IngresoDiarioDetailSerializers
    permission_classes=[IsAuthenticated]

    def get(self, request, ingresodiario_id):
        ingresodiario = get_object_or_404(IngresoDiario, pk=ingresodiario_id)
        serializer = self.serializer_class(instance=ingresodiario)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def put(self, request, ingresodiario_id):
        data = request.data
        ingresodiario = get_object_or_404(IngresoDiario, pk=ingresodiario_id)
        serializer = self.serializer_class(data=data, instance=ingresodiario)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, ingresodiario_id):
        ingresodiario = get_object_or_404(IngresoDiario, pk=ingresodiario_id)
        ingresodiario.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
