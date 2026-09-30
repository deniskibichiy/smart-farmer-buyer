from rest_framework import serializers
from apps.user.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    # Returns authenticated user details to the frontend
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 'role', 'phone_number',
        ]
        read_only_fields = ['id', 'role']


class RegisterSerializer(serializers.ModelSerializer):
    # For user registration. Handle frontend camelCase mapping, role normalization, password verification and secure user creation
    firstName = serializers.CharField(source='first_name', write_only=True)
    lastName = serializers.CharField(source='last_name', write_only=True)
    confirmPassword = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True, min_length=8)
    role = serializers.CharField(required=False, default=CustomUser.Role.BUYER)

    class Meta:
        model = CustomUser
        # Pick from frontend
        fields = ['email', 'username', 'firstName', 'lastName', 'password', 'confirmPassword', 'role',
        ]

    def validate_role(self, value):
        # Normalize lowercase frontend role input to model choices (which are in to be stored in caps)
        normalized_role = value.upper() # From frontend it's lower, now here it's upper.
        valid_roles = [CustomUser.Role.FARMER, CustomUser.Role.BUYER] # Role-based classification accepted per the User model definition
        if normalized_role not in valid_roles: # Do the two match?
            raise serializers.ValidationError("Invalid role selected.") # Technically, this is just a security feature at this point.
        return normalized_role

    def validate(self, attrs):
        # Verify if passwords match in case js validation is bypassed
        if attrs.get('password') != attrs.get('confirmPassword'):
            raise serializers.ValidationError({"confirmPassword": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        # Save the cleaned entry for User credentials
        validated_data.pop('confirmPassword', None) # Remove confirm password to avoid field issues and either way, it shouldn't be stored in the first place.

        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            role=validated_data.get('role', CustomUser.Role.BUYER)
        )
        return user


class LoginSerializer(serializers.Serializer):
    # Authenticate user via email and password
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        try: user = CustomUser.objects.get(email=email) # Get user 
        except CustomUser.DoesNotExist: raise serializers.ValidationError({"detail": "Invalid email or password."})

        if not user.check_password(password):
            raise serializers.ValidationError({"detail": "Invalid email or password."})

        if not user.is_active:
            raise serializers.ValidationError({"detail": "User account is disabled."})

        attrs['user'] = user
        return attrs