# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.contrib.auth.models import AbstractUser, UserManager
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.db.models import Count, Min, Sum, Avg
import operator
class CustomManager(models.Manager):
    def with_bookings(self):
        filter_book = Booking.objects.all().distinct('user_id')
        book = []
        for each in filter_book:
            book.append(each.user_id)
        return User.objects.filter(id__in=book)

    def with_transaction_and_booking(self):
        filter_wallet = WalletTransaction.objects.all()
        book = []
        for each in filter_wallet:
            book.append(each.wallet_id)
        return User.objects.filter(wallet__id__in=book)

    def no_bookings(self):
        filter_user = User.objects.all()
        book_id = [4]
        filter_bookings = Booking.objects.all().distinct('user_id')
        for each_book in filter_bookings:
            book_id.append(each_book.user_id)

        no_book = []
        for each in filter_user:
            if each.id in book_id:
                pass
            else:
                no_book.append(each.id)
        j = User.objects.filter(id__in=no_book)
        return j


    def with_transaction_total(self):
        self.k = Wallet.objects.values('id').annotate(transaction_total=Sum('transactions__total'))

        a = []
        b = 0
        for each in self.k:
            p = self.model(each)
            if self.k[b]["id"] == 1:
                p.transaction_total = self.k[0]["transaction_total"]
            elif self.k[b]["id"] == 2:
                p.transaction_total =self.k[1]["transaction_total"]
            elif self.k[b]["id"] == 3:
                p.transaction_total = self.k[2]["transaction_total"]
            a.append(p)
            b += 1

        return a



@python_2_unicode_compatible
class User(AbstractUser):
    g_objects = CustomManager()


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
    transaction_total = models.IntegerField(default=0)


class WalletTransaction(models.Model):
    wallet = models.ForeignKey(Wallet, related_name='transactions')
    booking = models.ForeignKey(Booking, null=True)
    total = models.IntegerField(default=0)
