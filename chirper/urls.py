"""chirper URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from chirps.views import ChirpList
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.views import logout
from django.core.urlresolvers import reverse_lazy
from users.views import RegisterUser

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^chirps/', include("chirps.urls")),
    url(r'^logout/$', logout, {'next_page':reverse_lazy('chirp_list')},
        name='logout'),
    url(r"^register/$", RegisterUser.as_view(), name="register"),
    url(r"^$", ChirpList.as_view()),
    url('^', include('django.contrib.auth.urls'))


]
