from django.contrib.auth.backends import ModelBackend

from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.contrib.auth import get_user_model
CustomUser = get_user_model()
import phonenumbers

def normalize_phone(phone, country="BB"):
    parsed = phonenumbers.parse(phone, country)
    if not phonenumbers.is_valid_number(parsed):
        raise ValueError("Invalid phone number")
    return phonenumbers.format_number(
        parsed,
        phonenumbers.PhoneNumberFormat.E164
    )


class EmailOrPhoneBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None or password is None:
            return None

        try:
            user = CustomUser.objects.get(
                Q(email=username) | Q(phone=username)
            )
        except CustomUser.DoesNotExist:
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
