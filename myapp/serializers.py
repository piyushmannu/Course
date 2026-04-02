from .models import *
from rest_framework import serializers
from django.contrib.auth.models import User

class categorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
