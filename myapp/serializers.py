from .models import *
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.Serializer):  # Changed from ModelSerializer
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, min_length=8)
    role = serializers.ChoiceField(choices=['student', 'teacher'])
    bio = serializers.CharField(required=False, allow_blank=True)
    phone_no = serializers.CharField(max_length=11, required=False, allow_blank=True)
    dob = serializers.DateField(required=False, allow_null=True)
    
    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists")
        return value
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data['role'],
            bio=validated_data.get('bio', ''),
            phone_no=validated_data.get('phone_no', ''),
            dob=validated_data.get('dob', None),
        )
        return user

# class UserSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only = True)

#     class Meta:
#         model = User
#         fields = ['username','email','password','role','bio','phone_no','dob']
#         extra_kwargs = {
#             'password' : {'write_only' : True},
#         }

#     def validate_role(self, value):
#         """ Ensure role is either student or a teacher"""
#         if value not in ['student','teacher']:
#             raise serializers.ValidationError("Role must be student or teacher")
#         return value

#     def create(self, validated_data):
#         user = User.objects.create_user(
#             username = validated_data['username'],
#             email = validated_data.get('email', ''),
#             password = validated_data['password'],
#             role = validated_data['role'],
#             bio = validated_data.get('bio', ''),
#             phone_no = validated_data.get('phone_no', ''),
#             dob = validated_data.get('dob',None),
#         )
#         return user

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