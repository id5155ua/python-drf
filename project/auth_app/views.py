from django.contrib.auth import authenticate, get_user_model
from django.shortcuts import render, redirect
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_201_CREATED

from .serializers import UserSerializer
from .models import User


User = get_user_model()

def VerificationView(request, verification_key):
    
    try:
        user = User.objects.get(verification_key=verification_key)
    except User.DoesNotExist:
        return render(request, 'invalid_token.html')
    user.is_verified = True
    user.save()
    return redirect('login')


class RegisterView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer
    
    def post(self, request, format='json'):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        if email is None or password is None:
            return Response({'error': 'Please provide both email and password'},
                            status=HTTP_400_BAD_REQUEST)
        user = authenticate(username=email, password=password)
        if not user:
            return Response({'error': 'Invalid Credentials'},
                            status=HTTP_400_BAD_REQUEST)
        token, _ = Token.objects.get_or_create(user=user)
        response = Response({'token': token.key, 'email': user.email}, status=HTTP_200_OK)
        response['Authorization'] = f"Token {token.key}"
        return response


class LogoutView(GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        """Log out the current user by removing their authentication token."""
        request.user.auth_token.delete()
        return Response({'status': 'success', 'message': 'Successfully logged out.'})
    
    
