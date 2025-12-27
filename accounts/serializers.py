from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.validators import validate_email
from django.core.exceptions import ValidationError as DjangoValidationError
import phonenumbers

User = get_user_model()



def normalize_phone(phone, country):
    try:
        parsed = phonenumbers.parse(phone, country)
        if not phonenumbers.is_valid_number(parsed):
            raise serializers.ValidationError({"error":"Invalid phone number format"})
        return phonenumbers.format_number(
            parsed,
            phonenumbers.PhoneNumberFormat.E164
        )
    except phonenumbers.NumberParseException:
        raise serializers.ValidationError({"error":"Invalid phone number format"})



class RegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'email',
            'full_name',
            'phone',
            'country_code',
            'password',
            'confirm_password',
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')
        email = attrs.get('email')
        phone = attrs.get('phone')
        country_code = attrs.get('country_code')

        if not password or not confirm_password:
            raise serializers.ValidationError("Password and confirm password are required")

        if password != confirm_password:
            raise serializers.ValidationError("Passwords do not match")

        if email and User.objects.filter(email=email).exists():
            raise serializers.ValidationError("A user with this email already exists")

        if phone:
            normalized_phone = normalize_phone(phone, country_code)
            if User.objects.filter(phone=normalized_phone).exists():
                raise serializers.ValidationError("A user with this phone number already exists")
            attrs['phone'] = normalized_phone

        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password', None)
        user = User.objects.create_user(**validated_data)
        return user



class LoginSerializer(serializers.Serializer):
    email_or_phone = serializers.CharField()
    password = serializers.CharField(write_only=True)
    country_code = serializers.CharField(required=False)

    def validate(self, attrs):
        email_or_phone = attrs.get('email_or_phone')
        password = attrs.get('password')
        country_code = attrs.get('country_code')
        if not country_code:
            raise serializers.ValidationError({"error":"Country code is required"})

        if not email_or_phone or not password:
            raise serializers.ValidationError({"error":"Email/Phone and password are required"})

        user = None

        
        try:
            validate_email(email_or_phone)
            is_email = True
        except DjangoValidationError:
            is_email = False

        try:
            if is_email:
                user = User.objects.get(email=email_or_phone)
            else:
                normalized_phone = normalize_phone(email_or_phone, country_code)
                user = User.objects.get(phone=normalized_phone)

        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid credentials")

        if not user.is_active:
            raise serializers.ValidationError("Account is not activated")

        if not user.check_password(password):
            raise serializers.ValidationError("Invalid credentials")

        attrs['user'] = user
        return attrs