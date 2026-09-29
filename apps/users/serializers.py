from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import IntegrityError
from rest_framework.exceptions import ValidationError as DRFValidationError
from .models import Member, Policy, UserPolicySignature

# 1. Member Serializer (Handles creating User + Member together)
class MemberSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    email = serializers.EmailField(source='user.email')
    password = serializers.CharField(write_only=True, source='user.password', required=True)

    class Meta:
        model = Member
        fields = [
            'id', 'username', 'email', 'password', 
            'name', 'phone', 'role', 'dividend_preference'
        ]

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        
        try:
            # 1. Create the built-in User
            user = User.objects.create_user(**user_data)
            
            # 2. Create the Member profile linked to the User
            member = Member.objects.create(user=user, **validated_data)
            return member
            
        except IntegrityError:
            # Catches duplicate usernames or emails
            raise DRFValidationError({"username": "A user with this username or email already exists."})
        except DjangoValidationError as e:
            # Catches Django's password validators (e.g. "This password is too short")
            raise DRFValidationError(e.message_dict if hasattr(e, 'message_dict') else e.messages)
        except Exception as e:
            # Catch any other unexpected errors
            raise DRFValidationError(str(e))

# 2. Custom Login Serializer (Allows Email or Username)
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        login_input = attrs.get('username')
        password = attrs.get('password')

        if '@' in login_input:
            try:
                user_obj = User.objects.get(email=login_input)
                attrs['username'] = user_obj.username
            except User.DoesNotExist:
                raise serializers.ValidationError("No account found with this email.")
        
        user = authenticate(
            request=self.context.get('request'),
            username=attrs['username'],
            password=password
        )

        if not user:
            raise serializers.ValidationError("Invalid credentials. Please try again.")

        refresh = self.get_token(user)
        
        # Return member data if they are a member, otherwise just basic info
        try:
            member_data = MemberSerializer(Member.objects.get(user=user)).data
        except Member.DoesNotExist:
            member_data = {'username': user.username, 'role': 'Super Admin'}

        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': member_data
        }
        return data

class PolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = Policy
        fields = '__all__'

class UserPolicySignatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPolicySignature
        fields = '__all__'