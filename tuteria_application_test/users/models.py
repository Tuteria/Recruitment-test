# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.contrib.auth.models import AbstractUser, UserManager
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Sum
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

class UserQuerySet(models.QuerySet):

    def with_bookings(self):
        queryset = self.filter(
            wallet__transactions__booking__isnull=False).distinct()

        return queryset

    def with_transaction_total(self):
        queryset = self.filter(wallet__isnull=False)
        queryset = queryset.annotate(
            transaction_total=Sum('wallet__transactions__total')
            )
        
        return queryset

    def with_transaction_and_booking(self):
        """Return users with both transactions and bookings."""
        queryset = self.filter(
            wallet__isnull=False, wallet__transactions__isnull=False
            )

        return queryset

    def no_bookings(self):
        queryset = self.with_transaction_total().filter(orders__isnull=True)

        return queryset

@python_2_unicode_compatible
class User(AbstractUser):

    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = models.CharField(_('Name of User'), blank=True, max_length=255)
    g_objects = UserQuerySet.as_manager()
    
    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'username': self.username})


class Booking(models.Model):
    user = models.ForeignKey(User, null=True, related_name='orders')
    order = models.CharField(max_length=12, primary_key=True, db_index=True)
    status = models.CharField(max_length=12, default='not_started')
    CANCELLED = "cancelled"
    COMPLETED = "completed"
    SCHEDULED = "scheduled"
    NOT_STARTED = "not_started"
    


class Wallet(models.Model):
    owner = models.OneToOneField(User, related_name='wallet')


class WalletTransaction(models.Model):
    wallet = models.ForeignKey(Wallet, related_name='transactions')
    booking = models.ForeignKey(Booking, null=True)
    total = models.DecimalField(decimal_places=2, max_digits=10)
