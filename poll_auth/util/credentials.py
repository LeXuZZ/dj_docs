from django.contrib.auth import authenticate

from poll_auth.models import PollUser
from poll_auth.util import constant


class CredentialsValidationException(Exception):
    pass


class LoginCredentials:
    def __init__(self, **kwargs):
        self.email = kwargs.get('email')
        self.password = kwargs.get('password')

    @property
    def email(self):
        return self._email

    @property
    def password(self):
        return self._password

    @property
    def user(self):
        return self.user

    @email.setter
    def email(self, email):
        if not email: raise CredentialsValidationException(constant.ErrorMessage.LOGIN_EMAIL_BLANK)
        self._email = email

    @password.setter
    def password(self, password):
        if not password: raise CredentialsValidationException(constant.ErrorMessage.LOGIN_PASSWORD_BLANK)
        self._password = password

    @user.getter
    def user(self):
        user = authenticate(username=self.email, password=self.password)
        if not user: raise CredentialsValidationException(constant.ErrorMessage.LOGIN_AUTHENTICATION_ERROR)
        if not user.is_active: raise CredentialsValidationException(constant.ErrorMessage.LOGIN_USER_IS_NOT_ACTIVE)
        return user


class RegistrationCredentials:
    def __init__(self, **kwargs):
        self.email = kwargs.get('email')
        self.password = kwargs.get('password')
        self.password_confirmation = kwargs.get('password_confirmation')
        self.firstname = kwargs.get('firstname')
        self.lastname = kwargs.get('lastname')
        self.middlename = kwargs.get('middlename')

    @property
    def email(self):
        return self._email

    @property
    def password(self):
        return self._password

    @property
    def password_confirmation(self):
        return self._password_confirmation

    @property
    def firstname(self):
        return self._firstname

    @property
    def lastname(self):
        return self._lastname

    @property
    def middlename(self):
        return self._middlename

    @email.setter
    def email(self, e):
        if not e: raise CredentialsValidationException(constant.ErrorMessage.REGISTRATION_BLANK_CREDENTIALS)
        try:
            PollUser.objects.get(email=e)
            raise CredentialsValidationException(constant.ErrorMessage.REGISTRATION_USER_EXISTS)
        except PollUser.DoesNotExist:
            self._email = e

    @password.setter
    def password(self, p):
        if not p: raise CredentialsValidationException(constant.ErrorMessage.REGISTRATION_BLANK_CREDENTIALS)
        self._password = p

    @password_confirmation.setter
    def password_confirmation(self, pc):
        if not pc: raise CredentialsValidationException(constant.ErrorMessage.REGISTRATION_BLANK_CREDENTIALS)
        if not pc == self._password: raise CredentialsValidationException(constant.ErrorMessage.REGISTRATION_PASSWORD_NOT_MATCH)
        self._password_confirmation = pc

    @firstname.setter
    def firstname(self, f):
        if not f: raise CredentialsValidationException(constant.ErrorMessage.REGISTRATION_BLANK_CREDENTIALS)
        self._firstname = f

    @lastname.setter
    def lastname(self, l):
        if not l: raise CredentialsValidationException(constant.ErrorMessage.REGISTRATION_BLANK_CREDENTIALS)
        self._lastname = l

    @middlename.setter
    def middlename(self, m):
        if not m: raise CredentialsValidationException(constant.ErrorMessage.REGISTRATION_BLANK_CREDENTIALS)
        self._middlename = m

    def poll_user_data(self):
        return {
            'email': self.email,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'middlename': self.middlename,
            'password': self.password,
        }

    def redis_data(self, registration_hash=None):
        return {**self.poll_user_data(), **{'registration_hash': registration_hash, 'service': 'registration'}}