import logging

import time

import stripe
from chirps.forms import ChirpForm
from chirps.models import Chirp
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.views.generic import UpdateView, ListView, DetailView, CreateView, View

logger = logging.getLogger(__name__)

class ChirpList(ListView):
    model = Chirp
    paginate_by = 20

    def get_queryset(self):
        #time.sleep(10)
        qs = Chirp.objects.select_related().all()

        if "user" in self.request.GET:
            qs = qs.filter(user__username=self.request.GET["user"])

        qs = qs.order_by("-created_at")
        logger.debug("ChirpList returned {} chirps".format(qs.count()))
        return qs


class ChirpDetail(DetailView):
    model = Chirp
    pk_url_kwarg = 'id'
    queryset = Chirp.objects.select_related().all()

    def get_context_data(self, **kwargs):
        #time.sleep(10)
        context = super().get_context_data(**kwargs)

        author_list = self.request.session.get("author_list", {})
        author_list[self.object.user.username] = \
            author_list.get(self.object.user.username, 0) + 1
        self.request.session['author_list'] = author_list

        context["time_run"] = timezone.now()
        context["strip_key"] = settings.STRIPE_PUBLISHABLE_KEY
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


def chirp_donate(request):
    token = request.POST["stripeToken"]

    stripe.api_key = settings.STRIPE_SECRET_KEY

    amount = int(float(request.POST['amount']) * 100)
    try:
        charge = stripe.Charge.create(
            amount=amount,  # amount in cents, again
            currency="usd",
            source=token,
            description="Donation to chirp"
        )
    except stripe.error.CardError as e:
        # The card has been declined
        pass

    return HttpResponseRedirect(reverse('chirp_list'))
