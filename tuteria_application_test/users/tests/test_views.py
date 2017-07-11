import json
from django.test import RequestFactory
from mock import patch
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory
from test_plus.test import TestCase
from .factories import UserFactory, BookingFactory, WalletTransactionFactory
from ..views import (
    UserRedirectView,
    UserUpdateView,
    UserDetailView,
)
from ..serializers import UserSerializer


class BaseUserTestCase(TestCase):

    def setUp(self):
        self.user = self.make_user()
        self.factory = RequestFactory()


class TestUserRedirectView(BaseUserTestCase):

    def test_get_redirect_url(self):
        # Instantiate the view directly. Never do this outside a test!
        view = UserRedirectView()
        # Generate a fake request
        request = self.factory.get('/fake-url')
        # Attach the user to the request
        request.user = self.user
        # Attach the request to the view
        view.request = request
        # Expect: '/users/testuser/', as that is the default username for
        #   self.make_user()
        self.assertEqual(
            view.get_redirect_url(),
            '/users/testuser/'
        )


class TestUserUpdateView(BaseUserTestCase):

    def setUp(self):
        # call BaseUserTestCase.setUp()
        super(TestUserUpdateView, self).setUp()
        # Instantiate the view directly. Never do this outside a test!
        self.view = UserUpdateView()
        # Generate a fake request
        request = self.factory.get('/fake-url')
        # Attach the user to the request
        request.user = self.user
        # Attach the request to the view
        self.view.request = request

    def test_get_success_url(self):
        # Expect: '/users/testuser/', as that is the default username for
        #   self.make_user()
        self.assertEqual(
            self.view.get_success_url(),
            '/users/testuser/'
        )

    def test_get_object(self):
        # Expect: self.user, as that is the request's user object
        self.assertEqual(
            self.view.get_object(),
            self.user
        )

class DjangoRestFrameworkUsageApiTestCase(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = UserFactory(first_name='Biola', last_name='Oyeniyi',
                                email='b_oye@example.com', id=1)
        self.booking = BookingFactory(user=self.user, order='ABCDEFGHIJKL')
        WalletTransactionFactory(booking=self.booking,
                                 wallet=self.user.wallet, total=20000)
        self.patch = patch('tuteria_application_test.users.views.UserSerializer')
        self.mock = self.patch.start()
        self.mock.return_value = UserSerializer(UserFactory.get_user(self.user))

    def tearDown(self):
        self.patch.stop()

    def test_post_request_for_api_view(self):
        data = {
            "email": self.user.email,
        }
        url = self.reverse('users:the_api', self.user.pk)
        response = self.json_post(data, url=url)

        self.mock.assert_called_once_with(self.user)
        data2 = json.loads(response.content.decode('utf-8'))
        self.assertEqual(data2, {
            'first_name': 'Biola',
            'last_name': 'Oyeniyi',
            'booking_order': ['ABCDEFGHIJKL'],
            'transaction_total': '20000.00'
        })

    def json_post(self, data, cls=UserDetailView, url=None):
        request = self.factory.post(
            url, json.dumps(data), 'json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',)
        return cls.as_view()(request)

    def test_api_view_get_request_returns_valid_response(self):
        response = self.client.get(self.reverse('users:the_api', self.user.pk))
        self.mock.assert_called_once_with(self.user)
        data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(data, {
            'first_name': 'Biola',
            'last_name': 'Oyeniyi',
            'booking_order': ['ABCDEFGHIJKL'],
            'transaction_total': '20000.00'
        })
