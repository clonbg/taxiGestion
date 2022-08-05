from django.shortcuts import render, get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from .models import User
from . import serializers
from rest_framework.permissions import IsAuthenticated

class UserCreateView(generics.GenericAPIView):
    serializer_class = serializers.UserCreationSerializers
    permission_classes=[IsAuthenticated]
    queryset = User.objects.order_by('-id')

    def get(self, request):
        serializer = self.serializer_class(instance=self.queryset.all(), many=True)
        return Response(data=serializer.data,status=status.HTTP_200_OK)

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
        
    def put(self, request, user_id):
        data=request.data
        user=get_object_or_404(User, pk=user_id)
        serializer=self.serializer_class(data=data,instance=user)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data,status=status.HTTP_200_OK)
        return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)