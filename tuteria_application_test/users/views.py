# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import json
from django.core.urlresolvers import reverse
from django.views.generic import DetailView, ListView, RedirectView, UpdateView, View
from braces.views import CsrfExemptMixin, JsonRequestResponseMixin, JSONResponseMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import User, Wallet
from rest_framework.views import APIView
from .serializers import UserSerializer, ResponseSerializer
from rest_framework.response import Response


class UserApiView(APIView):
    def get(self, request):
        user = User.g_objects.get(email='b_oye@example.com')

        serializer = UserSerializer(user)
        if serializer.is_valid():
            return Response(ResponseSerializer(first_name = user.first_name,
                                                last_name = user.last_name,
                                                booking_order = user.booking_order,
                                                transaction_total = 20000.00))

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = serializer.validated_data
            user = User.g_objects.get(email=data["email"])
            return Response(ResponseSerializer(first_name = user.first_name,
                                                last_name = user.last_name,
                                                booking_order = user.booking_order,
                                                transaction_total = 20000.00))

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
