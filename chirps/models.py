import datetime
import time

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.text import slugify


class Chirp(models.Model):

    message = models.CharField(max_length=150)
    subject = models.CharField(max_length=50, help_text="Short version as a title of longer chirp message")
    created_at = models.DateTimeField(auto_now_add=True, db_index=True,
                                      verbose_name="Created")
    modified_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User)
    image = models.ImageField(upload_to="profile/", null=True, blank=True)
    archived = models.BooleanField(default=False)
    slug = models.SlugField(max_length=50, null=True, blank=True)


    def is_recent(self):
        return timezone.now() - datetime.timedelta(days=1) <= self.created_at

    def __str__(self):
        return "{} says {}".format(self.user.username, self.subject)

    @property
    def tag_count(self):
        return self.tag_set.count()

    def save(self, **kwargs):
        if not self.slug:
            self.slug = slugify(self.subject)

        super().save(**kwargs)

    # @cached_property
    def slow_runner(self):
        time.sleep(5)
        return "I slept for {} seconds for id {}".format(5, self.id)


    class Meta:
        ordering = ["-created_at", "id"]
        default_related_name = "chirps"
        get_latest_by = "created_at"
        verbose_name = "chirp"
        verbose_name_plural = "chirps"
        # index_together = [["user", "subject"]]
        # unique_together = (("city", "state"),)


class Pledge(models.Model):
    user = models.ForeignKey(User, related_name='pledges')
    chirp = models.ForeignKey(Chirp, related_name='pledges')
    amount = models.IntegerField()
    charge_id = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


class Tag(models.Model):
    chirps = models.ManyToManyField(Chirp)
    name = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Name: {} Posted At: {}".format(self.name, self.created_at)


# class HashTag(models.Model):
#     text = models.CharField(max_length=10)
#     created_at = models.DateTimeField(auto_now_add=True)
#     modified_at = models.DateTimeField(auto_now=True)
#
#     class Meta:
#         abstract = True
#
#
# class UserHashTag(HashTag):
#     user = models.ForeignKey(User)
#
# class ChirpHashTag(HashTag):
#     chirp = models.ForeignKey(Chirp)