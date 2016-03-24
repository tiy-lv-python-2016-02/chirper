import datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Chirp(models.Model):

    message = models.CharField(max_length=150)
    subject = models.CharField(max_length=50, help_text="Short version as a title of longer chirp message")
    created_at = models.DateTimeField(auto_now_add=True, db_index=True,
                                      verbose_name="Created")
    modified_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User)
    #email = models.EmailField(max_length=50, validators=...)


    def is_recent(self):
        return timezone.now() - datetime.timedelta(days=1) <= self.created_at

    def __str__(self):
        return "{} says {}".format(self.user.username, self.subject)

    @property
    def tag_count(self):
        return self.tag_set.filter(user__username="kevin").count()


class Tag(models.Model):
    chirps = models.ManyToManyField(Chirp)
    name = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Name: {} Posted At: {}".format(self.name, self.created_at)

# class Favorite(models.Model):
#     FUNNY = "F"
#     INTERESTING = "I"
#     SAD = "S"
#     NO_REASON = "NR"
#     reasons = (
#         (FUNNY, 'Funny'),
#         (INTERESTING, "Interesting"),
#         (SAD, "Sad"),
#         (NO_REASON, "No Reason")
#     )
#
#     user = models.ForeignKey(User)
#     chirp = models.ForeignKey(Chirp)
#     why = models.CharField(max_length=3, choices=reasons, default=NO_REASON)