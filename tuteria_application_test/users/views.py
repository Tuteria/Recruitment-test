# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import json
from django.core.urlresolvers import reverse
from django.views.generic import DetailView, ListView, RedirectView, UpdateView, View
from braces.views import CsrfExemptMixin, JsonRequestResponseMixin, JSONResponseMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response

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


class UserApiView(APIView):
    """API view for the user model."""
    
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user)

        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        data = json.loads(request.data)
        user = User.objects.get(email=data.get('email'))
        serializer = UserSerializer(user)

        return JsonResponse(serializer.data)
