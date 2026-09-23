from rest_framework import generics, viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import Member, Policy, UserPolicySignature
from .serializers import MemberSerializer, RegisterSerializer, PolicySerializer, UserPolicySignatureSerializer

class RegisterView(generics.CreateAPIView):
    queryset = Member.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

class MyProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = MemberSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Get the Member profile attached to the logged-in User.
        # If it doesn't exist (e.g., for a superuser created via CLI), create it automatically.
        member, created = Member.objects.get_or_create(
            user=self.request.user,
            defaults={
                'name': self.request.user.username,
                'role': 'Super Admin' if self.request.user.is_superuser else 'Member'
            }
        )
        return member

class PolicyViewSet(viewsets.ModelViewSet):
    queryset = Policy.objects.all()
    serializer_class = PolicySerializer
    permission_classes = [IsAuthenticated]

class SignPolicyView(generics.CreateAPIView):
    queryset = UserPolicySignature.objects.all()
    serializer_class = UserPolicySignatureSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # The UserPolicySignature model expects a Member instance, not a User instance
        member = Member.objects.get(user=self.request.user)
        serializer.save(user=member)