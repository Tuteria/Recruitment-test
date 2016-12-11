# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.contrib.auth.models import AbstractUser, UserManager
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

class UserCustomQuerySet(models.query.QuerySet):
    def with_bookings(self):
        return self.filter(with_bookings=True)
    def no_bookings(self):
        return self.filter(with_bookings=False)
    def with_transaction_and_booking(self):
        self.filter(transaction_and_booking=True)


class CustomManager(UserManager):
    def get_queryset(self):
        return UserCustomQuerySet(self.model, using=self._db)
    def with_bookings(self):
        return self.get_queryset().with_bookings()
    def no_bookings(self):
        return self.get_queryset().no_bookings()
    def with_transaction_and_booking(self):
        return self.get_queryset().with_transaction_and_booking()

@python_2_unicode_compatible
class User(AbstractUser):
    g_objects = CustomManager()
    with_bookings = models.BooleanField(default=False)
    transaction_and_booking = models.BooleanField(default=False)
    transaction_total = models.DecimalField(max_digits=8, decimal_places=2, default=00.00)

    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = models.CharField(_('Name of User'), blank=True, max_length=255)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'username': self.username})


class Booking(models.Model):
    user = models.ForeignKey(User, null=True, related_name='orders')
    order = models.CharField(max_length=12, primary_key=True, db_index=True)


class Wallet(models.Model):
    owner = models.OneToOneField(User, related_name='wallet')


class WalletTransaction(models.Model):
    wallet = models.ForeignKey(Wallet, related_name='transactions')
    booking = models.ForeignKey(Booking, null=True)
    total = models.DecimalField(decimal_places=2, max_digits=10)
