from .models import *
from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','email','password','role','bio','phone_no','dob']

    def create(self, validated_data):
        user = User.objects.create_user(
            username = validated_data['username',],
            email = validated_data.get('email', ''),
            password = validated_data['password'],
            role = validated_data['role'],
            bio = validated_data.get('bio', ''),
            phone_no = validated_data.get('phone_no', ''),
            dob = validated_data.get('dob', ""),
        )
        return user

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