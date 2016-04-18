from api.views import DetailUpdateDeleteChirp, DetailUser, \
    ListCreateChirp, ListPledge, PledgeDetail, CreateCharge
from django.conf.urls import url
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    url(r"^chirps/$", ListCreateChirp.as_view(), name="list_create_chirp"),
    url(r"^chirps/(?P<pk>\d+)/$", DetailUpdateDeleteChirp.as_view(),
        name="detail_update_delete_chirp"),
    url(r"^users/(?P<pk>\d+)/$", DetailUser.as_view(), name="detail_user"),
    url(r"^api-token-auth/$", obtain_auth_token),
    url(r"^pledges/$", ListPledge.as_view(), name="list_pledge"),
    url(r"^pledges/(?P<pk>\d+)/$", PledgeDetail.as_view(),
        name="detail_pledge"),
    url(r"^charges/$", CreateCharge.as_view(), name="create_charge")
]