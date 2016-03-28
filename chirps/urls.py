from chirps.views import list_chirps, chirp_detail
from django.conf.urls import url

urlpatterns = [
    url(r'^$', list_chirps, name="chirp_list"),
    url(r'^(?P<id>\d+)/$', chirp_detail, name="chirp_detail")
]