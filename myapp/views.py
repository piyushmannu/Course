from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import *
from rest_framework import status
from .serializers import *
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated,AllowAny
from django.contrib.auth import get_user_model,authenticate
from .permission import IsTeacher, IsStudent, IsTeacherOrReadOnly, IsEnrolledStudent, IsOwnerOrReadOnly

User = get_user_model()
# Create your views here.
@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()

        #Auto generate the JWT tokens after register
        refresh = RefreshToken.for_user(user)

        return Response({
            "message" : f"{user.role.capitalize()} account created successfully",
            "username": user.username,
            "role" : user.role,
            "access_token" : str(refresh.access_token()),
            "refresh_token" : str(refresh),
        }, status = status.HTTP_201_CREATED)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET','POST'])
# @permission_classes([IsTeacherOrReadOnly])
# def enter_category(request):

#     #get read all the categories from DB
#     if request.method == "GET":
#         categories = Category.objects.all()
#         serializer = categorySerializer(categories, many = True)
#         return Response(serializer.data, status = status.HTTP_200_OK)

#     #to enter a new data
#     if request.method == "POST":
#         serializer = categorySerializer(data = request.data)
#         if serializer.is_valid():
#             serializer.save(created_by = request.user)
#             return Response(serializer.data, status = status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)        

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def enter_category(request):
    if request.method == "POST":
        serializer = categorySerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def enter_course(request):
    if request.method == "POST":
        serializer = courserserializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def enter_lesson(request):
    if request.method == "POST":
        serializer = lessonserializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status = status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def enrollment_status(request):
    if request.method == "POST":
        serializer = enrollserializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status = status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def coupon_status(request):
    if request.method == "POST":
        serializer = couponserializers(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status = status.HTTP_201_CREATED)
        return Response(serializer.errors,status = status.HTTP_BAD_REQUEST)

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def payment_status(request):
    if request.method == "POST":
        serializer = paymentserializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status = status.HTTP_201_CREATED)
        return Response(serializer.errors,status = status.HTTP_BAD_REQUEST)

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def review_posting(request):
    if request.method == "POST":
        serializer = reviewserializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status = status.HTTP_201_CREATED)
        return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)
