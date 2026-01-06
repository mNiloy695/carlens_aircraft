from .models import BookedModel
from rest_framework import serializers


class BookedModelSerializer(serializers.ModelSerializer):
    class Meta:
        model=BookedModel
        fields="__all__"
        