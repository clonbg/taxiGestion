from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import LicenciaCreationSerializers
from .models import Licencia


# Create your views here.
class HelloLicenciasView(generics.GenericAPIView):

    def get(self, request):
        return Response(data={"message": "Hola licencia"},
                        status=status.HTTP_200_OK)


class LicenciaCreateView(generics.GenericAPIView):
    serializer_class=LicenciaCreationSerializers
    queryset=Licencia.objects.all()

    def get(self, request):
        serializer_class=LicenciaCreationSerializers
        licencias=Licencia.objects.all()
        serializer = serializer_class(instance=licencias, many=True)
        return Response(data=serializer.data,status=status.HTTP_200_OK)

    def post(self, request):
        pass


class LicenciaDetailView(generics.GenericAPIView):

    def get(self, request, licencia_id):
        pass

    def put(self, request, licencia_id):
        pass

    def delete(self, request, licencia_id):
        pass