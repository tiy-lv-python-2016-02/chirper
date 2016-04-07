import logging

from chirps.forms import ChirpForm
from chirps.models import Chirp
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import UpdateView, ListView, DetailView, CreateView

logger = logging.getLogger(__name__)

class ChirpList(ListView):
    model = Chirp
    paginate_by = 5

    def get_queryset(self):
        qs = Chirp.objects.all()

        if "user" in self.request.GET:
            qs = qs.filter(user__username=self.request.GET["user"])

        qs = qs.order_by("-created_at")
        logger.debug("ChirpList returned {} chirps".format(qs.count()))
        return qs


class ChirpDetail(DetailView):
    model = Chirp
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        author_list = self.request.session.get("author_list", {})
        author_list[self.object.user.username] = \
            author_list.get(self.object.user.username, 0) + 1
        self.request.session['author_list'] = author_list

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
