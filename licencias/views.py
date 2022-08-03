from django.shortcuts import render, get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import LicenciaCreationSerializers, LicenciaDetailSerializers
from .models import Licencia
from rest_framework.permissions import IsAuthenticated


# Create your views here.
class HelloLicenciasView(generics.GenericAPIView):

    def get(self, request):
        return Response(data={"message": "Hola licencia"},
                        status=status.HTTP_200_OK)


class LicenciaCreateView(generics.GenericAPIView):
    serializer_class=LicenciaCreationSerializers
    queryset=Licencia.objects.all()
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


class LicenciaDetailView(generics.GenericAPIView):
    serializer_class = LicenciaDetailSerializers

    def get(self, request, licencia_id):
        licencia=get_object_or_404(Licencia, pk=licencia_id)
        serializer = self.serializer_class(instance=licencia)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
        

    def put(self, request, licencia_id):
        #2:31:47
        pass

    def delete(self, request, licencia_id):
        pass