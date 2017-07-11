# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.contrib.auth.models import AbstractUser, UserManager
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers


class UserQuerySet(models.QuerySet):

    def attached_bookings(self):
        return self.annotate(booking_count=models.Count('orders'))

    def with_bookings(self):
        return self.attached_bookings().filter(booking_count__gt=0)

    def with_transaction_total(self):
        return self.annotate(transaction_total=models.Sum('wallet__transactions__total')).exclude(transaction_total=None).order_by('-transaction_total')

    def with_transaction_and_booking(self):
        return self.with_transaction_total().exclude(orders=None)

    def no_bookings(self):
        return self.attached_bookings().filter(booking_count=0).with_transaction_total()


class NewUserManager(UserManager):

    def owned(self):
        return self.annotate(book=models.Count('orders__status')).exclude(orders=None)

    def bookings_aggs(self):
        owned = self.owned()
        cancelled = owned.filter(orders__status="cancelled").count()
        completed = owned.filter(orders__status="completed").count()
        not_started = self.owned().filter(orders__status="not_started").count()
        scheduled = self.owned().filter(orders__status="scheduled").count()
        return self.owned().annotate(completed=models.Value(completed, output_field=models.IntegerField()),
                                     cancelled=models.Value(
                                         cancelled, output_field=models.IntegerField()),
                                     not_started=models.Value(
                                         not_started, output_field=models.IntegerField()),
                                     scheduled=models.Value(
                                         scheduled, output_field=models.IntegerField())
                                     )


@python_2_unicode_compatible
class User(AbstractUser):

    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = models.CharField(_('Name of User'), blank=True, max_length=255)
    g_objects = UserQuerySet.as_manager()
    objects = NewUserManager()

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'username': self.username})


class Booking(models.Model):
    user = models.ForeignKey(User, null=True, related_name='orders')
    order = models.CharField(max_length=12, primary_key=True, db_index=True)

    NOT_STARTED = "not_started"
    COMPLETED = "completed"
    SCHEDULED = "scheduled"
    CANCELLED = "cancelled"

    BOOKING_STATUSES = (
        (NOT_STARTED, "not_started"),
        (COMPLETED, "completed"),
        (SCHEDULED, "scheduled"),
        (CANCELLED, "cancelled"),
    )

    status = models.CharField(
        max_length=256, choices=BOOKING_STATUSES, default=NOT_STARTED)


class Wallet(models.Model):
    owner = models.OneToOneField(User, related_name='wallet')


class WalletTransaction(models.Model):
    wallet = models.ForeignKey(Wallet, related_name='transactions')
    booking = models.ForeignKey(Booking, null=True)
    total = models.DecimalField(decimal_places=2, max_digits=10)
