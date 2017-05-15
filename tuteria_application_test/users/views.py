# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import json
from django.core.urlresolvers import reverse
from django.views.generic import DetailView, ListView, RedirectView, UpdateView, View
from braces.views import CsrfExemptMixin, JsonRequestResponseMixin, JSONResponseMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import User
from rest_framework.views import APIView
from rest_framework import serializers, status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

class UserSerializer(serializers.BaseSerializer):
    def to_representation(self, obj):
        return {
            'first_name': obj.first_name,
            'last_name': obj.last_name,
            'booking_order': obj.booking_order,
            'transaction_total': '%.2f' %obj.transaction_total
        }


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = 'username'
    slug_url_kwarg = 'username'


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse('users:detail',
                       kwargs={'username': self.request.user.username})


class UserUpdateView(LoginRequiredMixin, UpdateView):

    fields = ['name', ]

    # we already imported User in the view code above, remember?
    model = User

    # send the user back to their own page after a successful update
    def get_success_url(self):
        return reverse('users:detail',
                       kwargs={'username': self.request.user.username})

    def get_object(self):
        # Only get the User record for the user making the request
        return User.objects.get(username=self.request.user.username)


class UserListView(LoginRequiredMixin, ListView):
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = 'username'
    slug_url_kwarg = 'username'

class UserApiView(APIView):

    def get(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user)
        return Response(serializer.data)

    def post(self, request):
        data = json.loads(request.data)
        try:
            user = User.objects.get(email=data['email'])
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user)
        return Response(serializer.data, content_type="application/json")
