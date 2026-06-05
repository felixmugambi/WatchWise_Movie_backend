from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.contrib.auth import authenticate


class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):

        email = attrs.get("email")
        password = attrs.get("password")

        if not email or not password:
            raise serializers.ValidationError({
                "success": False,
                "message": "Email and password are required"
            })

        user = authenticate(
            username=email,
            password=password
        )

        if not user:
            raise serializers.ValidationError({
                "success": False,
                "message": "Invalid credentials"
            })

        if not user.is_active:
            raise serializers.ValidationError({
                "success": False,
                "message": "Account is disabled"
            })

        refresh = self.get_token(user)

        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "success": True,
            "message": "Login successful",
            "user": {
                "id": user.id,
                "email": user.email,
                "full_name": user.full_name
            }
        }