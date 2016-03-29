from chirps.forms import ChirpForm
from chirps.models import Chirp
from django.core.urlresolvers import reverse
from django.http import HttpResponse, Http404
from django.shortcuts import render, render_to_response, get_object_or_404, \
    redirect
from django.template import loader, Context
from django.utils import timezone
from django.views.generic import View


class ChirpList(View):

    def get(self, request):
        chirps = Chirp.objects.all().order_by("-created_at")

        return render(request, "chirps/chirp_list.html", {"chirps": chirps})

class ChirpDetail(View):

    def get(self, request, id):
        chirp = get_object_or_404(Chirp, pk=id)

        time_run = timezone.now()

        return render(request, "chirps/chirp_detail.html", {"chirp": chirp,
                                                        "time_run": time_run})

class ChirpCreate(View):

    def get(self, request):
        form = ChirpForm()

        return render(request, "chirps/chirp_create.html", {"form": form})

    def post(self, request):
        form = ChirpForm(request.POST)

        if form.is_valid():
            chirp = form.save(commit=False)
            chirp.user = request.user
            chirp.save()

            return redirect(reverse("chirp_list"))
        return render(request, "chirps/chirp_create.html", {"form": form})

def chirp_create(request):

    if request.method == "POST":
        form = ChirpForm(request.POST)

        if form.is_valid():
            chirp = form.save(commit=False)
            chirp.user = request.user
            chirp.save()

            return redirect(reverse("chirp_list"))
    else:
        form = ChirpForm()

    return render(request, "chirps/chirp_create.html", {"form": form})


def chirp_update(request, id):

    chirp = get_object_or_404(Chirp, pk=id)

    if request.method == "POST":
        form = ChirpForm(data=request.POST, instance=chirp)

        if form.is_valid():
            chirp = form.save(commit=False)
            chirp.user = request.user
            chirp.save()

            return redirect(reverse("chirp_list"))
    else:
        form = ChirpForm(instance=chirp)

    return render(request, "chirps/chirp_update.html", {"form": form, "chirp": chirp})


class ChirpUpdate(View):

    def get(self, request, id):
        chirp = get_object_or_404(Chirp, pk=id)

        form = ChirpForm(instance=chirp)

        return render(request, "chirps/chirp_update.html",
                      {"form": form, "chirp": chirp})

    def post(self, request, id):
        chirp = get_object_or_404(Chirp, pk=id)

        form = ChirpForm(data=request.POST, instance=chirp)

        if form.is_valid():
            chirp = form.save(commit=False)
            chirp.user = request.user
            chirp.save()

            return redirect(reverse("chirp_list"))
        return render(request, "chirps/chirp_update.html",
                      {"form": form, "chirp": chirp})