from rest_framework import serializers
from django.contrib.auth import get_user_model
import phonenumbers
User=get_user_model()

class RegistrationSerializer(serializers.ModelSerializer):
    confirm_password=serializers.CharField(write_only=True)
    class Meta:
        model=User
        fields=['email','full_name','phone','password','confirm_password','date_joined']
        read_only_fields=['date_joined']
        extra_kwargs={
            'password':{'write_only':True},
            'confirm_password':{'write_only':True},
        }
    def validate(self,attrs):
        password=attrs.get('password')
        confirm_password=attrs.get('confirm_password')
        if not password or not confirm_password:
            raise serializers.ValidationError("Password and Confirm Password are required")
        if password != confirm_password:
            raise serializers.ValidationError("Passwords do not match")
        
        email=attrs.get('email')
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("A user with this email already exists")
        phone=attrs.get('phone')
        
        try:
            parsed_phone=phonenumbers.parse(phone,None)
            if not phonenumbers.is_valid_number(parsed_phone):
                raise serializers.ValidationError("Invalid phone number format")
            phone=phonenumbers.format_number(parsed_phone,phonenumbers.PhoneNumberFormat.E164)
            attrs['phone']=phone
        except phonenumbers.NumberParseException:
            raise serializers.ValidationError("Invalid phone number format")
        if User.objects.filter(phone=phone).exists():
            raise serializers.ValidationError("A user with this phone number already exists")
      
        return attrs
    
    
    def create(self,validated_data):
        validated_data.pop('confirm_password',None)
        user=User.objects.create_user(**validated_data)
        return user