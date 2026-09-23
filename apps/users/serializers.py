from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Member, Policy, UserPolicySignature

# 1. Fix the MemberSerializer
class MemberSerializer(serializers.ModelSerializer):
    # These pull fields from the connected built-in User model
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    
    class Meta:
        model = Member
        fields = [
            'id', 
            'username', 
            'email', 
            'name', 
            'phone', 
            'role', 
            'dividend_preference'
        ]

# 2. Custom Login Serializer (Allows Email or Username)
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # The frontend sends the input as 'username'
        login_input = attrs.get('username')
        password = attrs.get('password')

        # If the input contains '@', treat it as an email
        if '@' in login_input:
            try:
                # Find the User by email
                user_obj = User.objects.get(email=login_input)
                # Swap the email for the actual username so SimpleJWT can authenticate it
                attrs['username'] = user_obj.username
            except User.DoesNotExist:
                raise serializers.ValidationError("No account found with this email.")
        
        # Now authenticate with the resolved username
        user = authenticate(
            request=self.context.get('request'),
            username=attrs['username'],
            password=password
        )

        if not user:
            raise serializers.ValidationError("Invalid credentials. Please try again.")

        # Generate the token using the parent class
        refresh = self.get_token(user)
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': MemberSerializer(Member.objects.get(user=user)).data
        }
        return data
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = Member
        fields = ['username', 'password', 'name', 'phone', 'role']

    def create(self, validated_data):
        user = Member.objects.create_user(**validated_data)
        return user

class PolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = Policy
        fields = '__all__'

class UserPolicySignatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPolicySignature
        fields = '__all__'