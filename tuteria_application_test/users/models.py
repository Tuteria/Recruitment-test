# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.contrib.auth.models import AbstractUser, UserManager
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

class CustomQuerySet(models.QuerySet):

    def with_bookings(self):
        return self.exclude(orders__isnull=True)

    def with_transaction_total(self):
        return self.filter(wallet__transactions__total__gt=0).annotate(transaction_total=models.Sum('wallet__transactions__total'))

    def with_transaction_and_booking(self):
        return self.with_bookings().filter(wallet__transactions__total__gt=0).annotate(transaction_total=models.Sum('wallet__transactions__total'))

    def no_bookings(self):
        return self.exclude(orders__isnull=False).annotate(transaction_total=models.Sum('wallet__transactions__total')).order_by('-id')


class CustomUserManager(UserManager):

    def get_queryset(self):
        return CustomQuerySet(self.model, using=self._db)

    def bookings_aggs(self):
        from django.db import connection
        with connection.cursor() as cursor:
            sql = """
                select u.*, (select count(user_id) from users_booking where status='completed' and user_id=u.id ) as completed,
                (select count(user_id) from users_booking where status='scheduled' and user_id=u.id ) as scheduled,
                (select count(user_id) from users_booking where status='cancelled' and user_id=u.id ) as cancelled,
                (select count(user_id) from users_booking where status='not_started' and user_id=u.id ) as not_started
                from users_user u
            """
            cursor.execute(sql)
            results = dictfetchall(cursor)
            result_list = []
            for row in results:
                completed = row.pop('completed')
                scheduled = row.pop('scheduled')
                not_started = row.pop('not_started')
                cancelled = row.pop('cancelled')
                user_obj = self.model(**row)
                user_obj.completed = completed
                user_obj.scheduled = scheduled
                user_obj.not_started = not_started
                user_obj.cancelled = cancelled
                result_list.append(user_obj)
        return result_list


@python_2_unicode_compatible
class User(AbstractUser):

    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = models.CharField(_('Name of User'), blank=True, max_length=255)

    g_objects = CustomQuerySet.as_manager()

    objects = CustomUserManager()

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'username': self.username})

    @property
    def booking_order(self):
        results = []
        orders = self.orders.all();
        for order in orders:
            results.append(order.order)
        return results


class Booking(models.Model):
    COMPLETED = "completed"

    SCHEDULED = "scheduled"

    CANCELLED = "cancelled"

    NOT_STARTED = "not_started"

    user = models.ForeignKey(User, null=True, related_name='orders')
    order = models.CharField(max_length=12, primary_key=True, db_index=True)
    status = models.CharField(max_length=40, default="not_started")


class Wallet(models.Model):
    owner = models.OneToOneField(User, related_name='wallet')


class WalletTransaction(models.Model):
    wallet = models.ForeignKey(Wallet, related_name='transactions')
    booking = models.ForeignKey(Booking, null=True)
    total = models.DecimalField(decimal_places=2, max_digits=10)
