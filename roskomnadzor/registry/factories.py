import factory
from django.contrib.auth import get_user_model

from registry.models import BlockRequest, Registry

User = get_user_model()


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: 'admin_{}'.format(n))
    email = factory.Sequence(lambda n: 'admin{0}@mail.com'.format(n))
    first_name = factory.Sequence(lambda n: 'Test Admin User {0}'.format(n))


class SuperUserFactory(UserFactory):
    is_staff = True
    is_superuser = True


class BlockRequestFactory(factory.DjangoModelFactory):

    class Meta:
        model = BlockRequest


class RegistryFactory(factory.DjangoModelFactory):
    ip = '127.0.0.1'
    user = factory.SubFactory(SuperUserFactory)

    class Meta:
        model = Registry
