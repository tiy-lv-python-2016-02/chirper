from chirps.models import Chirp
from django.http import HttpResponse, Http404
from django.shortcuts import render, render_to_response, get_object_or_404
from django.template import loader, Context
from django.utils import timezone


def list_chirps(request):
    chirps = Chirp.objects.all().order_by("-created_at")

    return render(request,"chirps/chirp_list.html", {"chirps": chirps})

def chirp_detail(request, id):
    chirp = get_object_or_404(Chirp, pk=id)

    time_run = timezone.now()

    return render(request, "chirps/chirp_detail.html", {"chirp": chirp,
                                                        "time_run": time_run})