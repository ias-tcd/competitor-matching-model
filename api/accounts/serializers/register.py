import logging

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.INFO)

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=(validate_password,))
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "password", "confirm_password"]

    def validate(self, attrs: dict) -> dict:
        if attrs["password"] != attrs["confirm_password"]:
            logger.error("[REGISTER]: User attempting to register with mismatched password!")
            raise serializers.ValidationError({"error_code": "Password fields don't match!"})
        return super().validate(attrs)

    def create(self, validated_data: dict):
        password = validated_data["password"]
        validated_data = {k: v for k, v in validated_data.items() if k not in ["confirm_password", "password"]}
        user = super().create({**validated_data, "username": validated_data["email"]})
        user.set_password(password)
        user.save()
        return user
