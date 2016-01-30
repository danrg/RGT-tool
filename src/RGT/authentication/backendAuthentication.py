from django.contrib.auth.models import User


class BackendAuthentication(object):
    def authenticate(self, email=None, password=None):
        if (email is None) or (password is None):
            return None  # Fail early.

        try:
            user = User.objects.get(email=email)

            pwd_valid = user.check_password(password)

            if pwd_valid:
                return user

        except User.DoesNotExist:
            pass  # Ignored

        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
