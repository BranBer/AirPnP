from django.contrib.auth.models import BaseUserManager

class MyUserManager(BaseUserManager):
    def create_user(self, username, personalEmail, first_name, last_name, home_address, password=None):
        if not username:
            raise ValueError("Users must have a username")
        if not personalEmail:
            raise ValueError("Users must have an email address")
        if not first_name:
            raise ValueError("Users must have a first name")
        if not last_name:
            raise ValueError("Users must have an last name")
        if not home_address:
            raise ValueError("Users must have a home address")

        user = self.model(
            username = username,
            personalEmail = self.normalize_email(personalEmail),
            first_name = first_name,
            last_name = last_name,
            home_address = home_address,
            password = password,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, personalEmail, first_name, last_name, home_address, password):
        user = self.create_user(
            username = username,
            personalEmail = self.normalize_email(personalEmail),
            password = password,
            first_name = first_name,
            last_name = last_name,
            home_address = home_address,
        )

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True

        user.save(using=self._db)
        return user

