# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import json
from django.core.urlresolvers import reverse
from django.views.generic import DetailView, ListView, RedirectView, UpdateView, View
from braces.views import CsrfExemptMixin, JsonRequestResponseMixin, JSONResponseMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from .models import User
from .serializers import UserSerializer


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

class UserApiView(CsrfExemptMixin, JsonRequestResponseMixin, View):
    def get(self, request, **kwargs):
        user = User.g_objects.filter(pk=kwargs['pk']).with_transaction_and_booking().first()
        data = UserSerializer(user).data
        return JsonResponse(data=data, status=2)

    def post(self, request, **kwargs):
        email = json.loads(self.request_json)['email']
        user = User.g_objects.filter(email=email).with_transaction_and_booking().first()
        data = UserSerializer(user).data
        return JsonResponse(data=data, status=2)