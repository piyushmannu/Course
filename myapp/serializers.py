from .models import *
from rest_framework import serializers
from django.contrib.auth.models import User

class categorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class courserserializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        queryset=Category.objects.all()
    )
    
    class Meta:
        model = Course
        fields = '__all__'

class lessonserializer(serializers.ModelSerializer):
    course = serializers.SlugRelatedField(
        slug_field='id',
        queryset=Course.objects.all()
    )
    class Meta:
        model = Lesson
        fields = '__all__'

class enrollserializer(serializers.ModelSerializer):
    course = serializers.SlugRelatedField(
        slug_field = 'title',
        queryset = Course.objects.all()
    )
    class Meta :
        model = Enrollment
        fields = '__all__'

class couponserializers(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = '__all__'

class paymentserializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ['transaction_id', 'created_at']

class reviewserializer(serializers.ModelSerializer):
    class Meta :
        model = review
        fields = '__all__'