import json

from chirps.models import Chirp
from django.contrib.auth.models import User
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View


@csrf_exempt
def list_create_chirp(request):

    if request.method == "GET":
        chirps = Chirp.objects.order_by("-created_at")
        content = serializers.serialize("json", chirps)
        return HttpResponse(content, content_type="application/json",
                            status=200)

    elif request.method == "POST":
        user = User.objects.first()

        data = json.loads(request.body.decode("UTF-8"))
        chirp = Chirp.objects.create(subject=data['subject'],
                                     message=data['message'],
                                     user=user)
        content = serializers.serialize("json", [chirp])
        return HttpResponse(content, content_type="application/json",)

    return HttpResponse("", status=405)

class DetailUpdateDeleteChirp(View):

    def get(self, *args, **kwargs):
        chirp = get_object_or_404(Chirp, pk=self.request.kwargs['chirp_id'])

        content = serializers.serialize("json", [chirp])
        return HttpResponse(content, status=200,
                            content_type="application/json")

    def put(self, *args, **kwargs):
        chirp = get_object_or_404(Chirp, pk=self.request.kwargs['chirp_id'])

        data = json.loads(self.request.body.decode("UTF-8"))
        chirp.message = data.get("message", chirp.message)
        chirp.subject = data.get("subject", chirp.subject)
        chirp.save()

        content = serializers.serialize("json", [chirp])
        return HttpResponse(content, status=200,
                            content_type="application/json")

    def delete(self, *args, **kwargs):
        chirp = get_object_or_404(Chirp, pk=self.request.kwargs['chirp_id'])
        chirp.delete()

        return HttpResponse([], status=204)