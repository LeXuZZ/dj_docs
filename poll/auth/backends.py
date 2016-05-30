from django.contrib.auth.hashers import check_password
from django.contrib.auth import get_user_model


class PollAuthBackend(object):

    def authenticate(self, username=None, password=None):
        try:
            user = get_user_model().objects.get(email__iexact=username)
            if check_password(password, user.password):
                return user
            else:
                return None
        except get_user_model().DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return get_user_model().objects.get(pk=user_id)
        except get_user_model.DoesNotExist:
            return None