from api.permissions import IsOwnerOrReadOnly
from api.serializers import ChirpSerializer, UserSerializer, PledgeSerializer, \
    ChargeSerializer
from chirps.models import Chirp, Pledge
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status


class TenResultsPaginator(PageNumberPagination):
    page_size = 10

class DetailUser(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ListCreateChirp(generics.ListCreateAPIView):
    queryset = Chirp.objects.all()
    serializer_class = ChirpSerializer
    pagination_class = TenResultsPaginator
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)

    def get_queryset(self):
        qs = super().get_queryset()

        params = self.request.query_params
        if "search" in params:
            qs = qs.filter(subject__contains=params["search"])

        return qs


class DetailUpdateDeleteChirp(generics.RetrieveUpdateDestroyAPIView):
    queryset = Chirp.objects.filter(archived=False)
    serializer_class = ChirpSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def perform_destroy(self, instance):
        instance.archived = True
        instance.save()


class ListPledge(generics.ListAPIView):
    queryset = Pledge.objects.all()
    serializer_class = PledgeSerializer


class PledgeDetail(generics.RetrieveAPIView):
    queryset = Pledge.objects.all()
    serializer_class = PledgeSerializer

class CreateCharge(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def post(self, request, format=None):
        serializer = ChargeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(None, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

