import json

from api.serializers import ChirpSerializer, UserSerializer
from chirps.models import Chirp
from django.contrib.auth.models import User
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

class DetailUser(APIView):

    def get(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except Chirp.DoesNotExist as e:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user)
        return Response(serializer.data)

@api_view(["GET", "POST"])
def list_create_chirp(request):

    if request.method == "GET":
        chirps = Chirp.objects.order_by("-created_at")
        serializer = ChirpSerializer(chirps, many=True,
                                     context={"request": request})

        return Response(serializer.data)

    elif request.method == "POST":
        user = User.objects.first()

        serializer = ChirpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DetailUpdateDeleteChirp(APIView):

    def get(self, request, pk):
        try:
            chirp = Chirp.objects.get(pk=pk)
        except Chirp.DoesNotExist as e:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ChirpSerializer(chirp, context={"request": request})
        return Response(serializer.data)


    def put(self, request, pk):
        try:
            chirp = Chirp.objects.get(pk=pk)
        except Chirp.DoesNotExist as e:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ChirpSerializer(chirp, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk):
        try:
            chirp = Chirp.objects.get(pk=pk)
        except Chirp.DoesNotExist as e:
            return Response(status=status.HTTP_404_NOT_FOUND)

        chirp.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)