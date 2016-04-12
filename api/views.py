from api.permissions import IsOwnerOrReadOnly
from api.serializers import ChirpSerializer, UserSerializer
from chirps.models import Chirp
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class TenResultsPaginator(PageNumberPagination):
    page_size = 10

class DetailUser(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ListCreateChirp(generics.ListCreateAPIView):
    queryset = Chirp.objects.order_by("-created_at")
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

