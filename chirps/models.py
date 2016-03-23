from django.contrib.auth.models import User
from django.db import models


class Chirp(models.Model):

    message = models.CharField(max_length=150)
    subject = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User)

    # remaining_count = models.IntegerField()
    # remaining_count = models.SmallIntegerField()
    # remaining_count = models.BigIntegerField()
    # is_popular = models.BooleanField()
    # is_popular = models.NullBooleanField()
    # created_date = models.DateField(auto_now_add=True)
    # cost = models.DecimalField(max_digits=7, decimal_places=2)
    # email = models.EmailField(max_length=200)
    # meta = models.OneToOneField(User)
    # favorites = models.ManyToManyField(Favorite)
