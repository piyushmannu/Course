from .models import *
from rest_framework import serializers
from django.contrib.auth.models import User

class categorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class courserserializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'