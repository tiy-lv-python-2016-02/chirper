from chirps.views import ChirpList, ChirpDetail, ChirpCreate, ChirpUpdate, \
    chirp_donate
from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page

urlpatterns = [
    url(r'^$', ChirpList.as_view(), name="chirp_list"),
    # url(r'^(?P<id>\d+)/$', cache_page(60 * 2)(ChirpDetail.as_view()),
    #     name="chirp_detail"),
    url(r'^(?P<id>\d+)/$', ChirpDetail.as_view(),
        name="chirp_detail"),
    url(r'^create/$', ChirpCreate.as_view(), name="chirp_create"),
    url(r'^update/(?P<pk>\d+)/$', ChirpUpdate.as_view(), name="chirp_update"),
    url(r"^chirp-donate/$", chirp_donate, name="chirp_donate"),
    url(r'^(?P<slug>[-\w]+)/$', ChirpDetail.as_view(), name="chirp_detail_slug"),
]