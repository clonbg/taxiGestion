from django.shortcuts import render, get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import VariosDiariosCreationSerializers, VariosDiariosDetailSerializers
from .models import VariosDiarios
from rest_framework.permissions import IsAuthenticated


class VariosDiariosCreateView(generics.GenericAPIView):
    serializer_class = VariosDiariosCreationSerializers
    queryset = VariosDiarios.objects.order_by('-id')

    # permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = self.serializer_class(instance=self.queryset.all(),
                                           many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


class VariosDiariosDetailView(generics.GenericAPIView):
    serializer_class = VariosDiariosDetailSerializers

    # permission_classes = [IsAuthenticated]

    def get(self, request, vario_diario_id):
        diario = get_object_or_404(VariosDiarios, pk=vario_diario_id)
        serializer = self.serializer_class(instance=diario)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def put(self, request, vario_diario_id):
        data = request.data
        diario = get_object_or_404(VariosDiarios, pk=vario_diario_id)
        serializer = self.serializer_class(data=data, instance=diario)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, varios_diarios_id):
        diario = get_object_or_404(VariosDiarios, pk=vario_diario_id)
        diario.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)