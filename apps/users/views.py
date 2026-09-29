from rest_framework import generics, viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import Member, Policy, UserPolicySignature
from .serializers import MemberSerializer, CustomTokenObtainPairSerializer, PolicySerializer, UserPolicySignatureSerializer

# --- Member ViewSet (For /api/members/) ---
class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all().order_by('id')
    serializer_class = MemberSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [AllowAny] # Or IsAuthenticated if only admins can add
        else:
            permission_classes = [IsAuthenticated]
        return super().get_permissions()

# --- Auth Views (For /api/auth/) ---
class CustomLoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class MyProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = MemberSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
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
        member = Member.objects.get(user=self.request.user)
        serializer.save(user=member)