import factory


class WalletFactory(factory.django.DjangoModelFactory):
    owner = factory.SubFactory('users.User', wallet=None)

    class Meta:
        model = 'users.Wallet'


class UserFactory(factory.django.DjangoModelFactory):
    username = factory.Sequence(lambda n: 'user-{0}'.format(n))
    email = factory.Sequence(lambda n: 'user-{0}@example.com'.format(n))
    password = factory.PostGenerationMethodCall('set_password', 'password')
    wallet = factory.RelatedFactory(WalletFactory, 'owner')

    class Meta:
        model = 'users.User'
        django_get_or_create = ('username', )

    @classmethod
    def get_user(self, user):
        from ..models import User
        return User.g_objects.filter(pk=user.pk).with_transaction_and_booking().first()


class BookingFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    order = factory.Sequence(lambda n: 'ACDESFFESG2{0}'.format(n))

    class Meta:
        model = 'users.Booking'


class WalletTransactionFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'users.WalletTransaction'
