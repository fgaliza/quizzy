import factory

from apps.users.models import AppUser


class AppUserFactory(factory.DjangoModelFactory):
    class Meta:
        model = AppUser

    name = 'Manny Calavera'
