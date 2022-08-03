from django.shortcuts import render, get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from .models import User
from . import serializers
from rest_framework.permissions import IsAuthenticated



class HelloTaxistasView(generics.GenericAPIView):
    def get(self, request):
        return Response(data={"message": "Hola taxista"}, status=status.HTTP_200_OK)


class UserCreateView(generics.GenericAPIView):
    serializer_class = serializers.UserCreationSerializers

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetailView(generics.GenericAPIView):
    serializer_class = serializers.UserDetailSerializers
    permission_classes=[IsAuthenticated]

    def get(self, request, user_id):
        user=get_object_or_404(User, pk=user_id)
        serializer = self.serializer_class(instance=user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
        

    """
    def put(self, request, licencia_id):
        data=request.data
        licencia=get_object_or_404(Licencia, pk=licencia_id)
        serializer=self.serializer_class(data=data,instance=licencia)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data,status=status.HTTP_200_OK)
        return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST) """