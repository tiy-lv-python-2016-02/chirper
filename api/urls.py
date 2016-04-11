from api.views import list_create_chirp, DetailUpdateDeleteChirp, DetailUser
from django.conf.urls import url

urlpatterns = [
    url(r"^chirps/$", list_create_chirp, name="list_create_chirp"),
    url(r"^chirps/(?P<pk>\d+)/$", DetailUpdateDeleteChirp.as_view(),
        name="detail_update_delete_chirp"),
    url(r"^users/(?P<pk>\d+)/$", DetailUser.as_view(), name="detail_user")
]