from rest_framework import generics, status
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import RegisterSerializer, MeSerializer


User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        return Response({
            "success": True,
            "message": "Account created successfully",
            "user": {
                "id": user.id,
                "email": user.email,
                "full_name": user.full_name
            }
        }, status=status.HTTP_201_CREATED)


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = MeSerializer(request.user)

        return Response({
            "success": True,
            "user": serializer.data
        })
