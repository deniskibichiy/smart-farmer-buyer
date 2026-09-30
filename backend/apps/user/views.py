from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from apps.user.models import CustomUser
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer


def generate_tokens(user):
    # Generate JWT access and refresh tokens for user instance
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class RegisterView(generics.CreateAPIView):
    # Validates, creates CustomUser in db and returns user object + the tokens
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data) # Picks data from serializer class
        serializer.is_valid(raise_exception=True) # Validate
        
        user = serializer.save() # Save user to db
        tokens = generate_tokens(user) # Call token function

        return Response({
            'message': 'Registration successful.',
            'user': UserSerializer(user).data,
            'tokens': tokens
        }, status=status.HTTP_201_CREATED)


class LoginView(generics.GenericAPIView):
    # Authenticates user and returns info + tokens
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.validated_data['user']
        tokens = generate_tokens(user)

        return Response({
            'message': 'Login successful.',
            'user': UserSerializer(user).data,
            'tokens': tokens
        }, status=status.HTTP_200_OK)


class UserProfileView(generics.RetrieveUpdateAPIView):
    # Returns profile details for the authenticated user
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user