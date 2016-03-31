from chirps.forms import ChirpForm
from chirps.models import Chirp
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponse, Http404
from django.shortcuts import render, render_to_response, get_object_or_404, \
    redirect
from django.template import loader, Context
from django.utils import timezone
from django.views.generic import UpdateView, ListView, DetailView, CreateView


class ChirpList(ListView):
    model = Chirp
    queryset = Chirp.objects.order_by("-created_at")
    paginate_by = 5


class ChirpDetail(DetailView):
    model = Chirp
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["time_run"] = timezone.now()
        return context


class ChirpCreate(LoginRequiredMixin, CreateView):
    model = Chirp
    form_class = ChirpForm
    success_url = reverse_lazy("chirp_list")
    template_name_suffix = "_create"
    # template_name = "chirps/chirp_create.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ChirpUpdate(LoginRequiredMixin, UpdateView):
    model = Chirp
    form_class = ChirpForm
    template_name = "chirps/chirp_update.html"

    def get_success_url(self):
        return reverse("chirp_detail", args=(self.object.id,))
