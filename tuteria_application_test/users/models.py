# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.contrib.auth.models import AbstractUser, UserManager
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from django.db.models import Sum, Count, Case, When


class CustomUserQuerySet(models.QuerySet):
    """Custom manager for User."""

    def with_bookings(self):
        """return users with bookings where the transaction > 1"""

        queryset = self.filter(
            wallet__transactions__booking__isnull=False).distinct()

        return queryset

    def with_transaction_total(self):
        """Get total transactions."""
        queryset = self.filter(wallet__isnull=False)
        queryset = queryset.annotate(
            transaction_total=Sum('wallet__transactions__total')
            )

        return queryset

    def with_transaction_and_booking(self):
        """Users with transactions and bookings."""
        queryset = self.filter(
            wallet__isnull=False, wallet__transactions__isnull=False
            )

        return queryset

    def no_bookings(self):
        """Users with no booking."""
        queryset = self.with_transaction_total().filter(orders__isnull=True)

        return queryset


class CustomUserManager(UserManager):
    """Custom queryset for the User model."""

    def bookings_aggs(self):
        """Annotate booking status."""
        queryset = self.get_queryset()
        queryset = queryset.annotate(
            completed=Count(
                Case(When(orders__status='completed', then=1))
            ),

            cancelled=Count(
                Case(When(orders__status='cancelled', then=1))
            ),

            scheduled=Count(
                Case(When(orders__status='scheduled', then=1))
            ),

            not_started=Count(
                Case(When(orders__status='not_started', then=1))
            )
        )

        return queryset


@python_2_unicode_compatible
class User(AbstractUser):

    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = models.CharField(_('Name of User'), blank=True, max_length=255)
    
    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'username': self.username})

    # register custom managers
    objects = CustomUserManager()
    g_objects = CustomUserQuerySet.as_manager()


class Booking(models.Model):
    
    # class attributes
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'
    SCHEDULED = 'scheduled'
    NOT_STARTED = 'not_started'

    BOOKING_CHOICES =(
        ('Completed', COMPLETED), ('Cancelled', CANCELLED),
        ('Scheduled', SCHEDULED), ('Not Started', NOT_STARTED)
        )

    user = models.ForeignKey(User, null=True, related_name='orders')
    order = models.CharField(max_length=12, primary_key=True, db_index=True)
    status = models.CharField(
        choices=BOOKING_CHOICES, max_length=12, default='not_started'
        )


class Wallet(models.Model):
    owner = models.OneToOneField(User, related_name='wallet')


class WalletTransaction(models.Model):
    wallet = models.ForeignKey(Wallet, related_name='transactions')
    booking = models.ForeignKey(Booking, null=True)
    total = models.DecimalField(decimal_places=2, max_digits=10)
