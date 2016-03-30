from chirps.views import ChirpList, ChirpDetail, ChirpCreate, ChirpUpdate
from django.conf.urls import url
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^$', ChirpList.as_view(), name="chirp_list"),
    url(r'^(?P<id>\d+)/$', ChirpDetail.as_view(), name="chirp_detail"),
    url(r'^create/$', ChirpCreate.as_view(), name="chirp_create"),
    url(r'^update/(?P<pk>\d+)/$', ChirpUpdate.as_view(), name="chirp_update")
]