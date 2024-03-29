from django.shortcuts import render, get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from . import serializers
from .models import IngresoSemanal
from rest_framework.permissions import IsAuthenticated

class IngresoSemanalCreateView(generics.GenericAPIView):
    serializer_class=serializers.IngresoSemanalCreationSerializers
    queryset=IngresoSemanal.objects.order_by('-id')
    permission_classes=[IsAuthenticated]

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

class IngresoSemanalDetailView(generics.GenericAPIView):
    serializer_class=serializers.IngresoSemanalDetailSerializers
    permission_classes=[IsAuthenticated]

    def get(self, request, ingresosemanal_id):
        ingresosemanal=get_object_or_404(IngresoSemanal, pk=ingresosemanal_id)
        serializer = self.serializer_class(instance=ingresosemanal)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def put(self, request, ingresosemanal_id):
        data=request.data
        ingresosemanal=get_object_or_404(IngresoSemanal, pk=ingresosemanal_id)
        serializer=self.serializer_class(data=data,instance=ingresosemanal)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data,status=status.HTTP_200_OK)
        return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, ingresosemanal_id):
        ingresosemanal=get_object_or_404(IngresoSemanal, pk=ingresosemanal_id)
        ingresosemanal.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

