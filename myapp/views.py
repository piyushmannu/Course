from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import *
from rest_framework import status
from .serializers import *
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated,AllowAny
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your views here.
@api_view(['GET','POST'])
def enter_category(request):
    if request.method == "POST":
        serializer = categorySerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class Helloview(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self,request):
        content = {'message': 'Hello, Greek'}
        return Response(content)
    
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    data = request.data

    required = ['username', 'email', 'password', 'role']
    
    # Bug 1 fixed: single loop, not nested
    for field in required:
        if field not in data:
            return Response(
                {'error': f'{field} is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

    # Bug 2 fixed: all checks are OUTSIDE the for loop
    if data['role'] not in ['student', 'teacher']:
        return Response(
            {'error': 'Role must be either student or teacher'},
            status=status.HTTP_400_BAD_REQUEST
        )

    if User.objects.filter(email=data['email']).exists():
        return Response(
            {'error': 'Email already exists'},  # Bug 5 fixed: dict not set
            status=status.HTTP_400_BAD_REQUEST
        )

    if User.objects.filter(username=data['username']).exists():
        return Response(
            {'error': 'Username already exists'},  # Bug 5 fixed
            status=status.HTTP_400_BAD_REQUEST
        )

    user = User.objects.create_user(
        username=data['username'],
        email=data['email'],
        password=data['password'],
        role=data['role']
    )

    refresh = RefreshToken.for_user(user)  # Bug 3 fixed: user not User

    return Response({
        'message': f'{user.role} account created successfully',
        'username': user.username,   # Bug 4 fixed: variable not string
        'email': user.email,         # Bug 4 fixed
        'role': user.role,           # Bug 4 fixed
        'access': str(refresh.access_token),
        'refresh': str(refresh)
    }, status=status.HTTP_201_CREATED)