from api.views import list_create_chirp, DetailUpdateDeleteChirp
from django.conf.urls import url

urlpatterns = [
    url(r"^chirps/$", list_create_chirp, name="list_create_chirp"),
    url(r"^chirps/(?P<chirp_id>)\d+/$", DetailUpdateDeleteChirp.as_view(),
        name="detail_update_delete_chirp")
]