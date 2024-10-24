from rest_framework import serializers
from .models import CustomFile


class CustomFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomFile
        fields = ['file']
