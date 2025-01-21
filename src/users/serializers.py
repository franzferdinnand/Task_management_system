from django.contrib.auth.models import User
from rest_framework import serializers
from utils.password_validation import validate_password


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "password",
            "confirm_password",
            "is_active",
            "is_staff",
        ]
        read_only_fields = ["password", "confirm_password", "is_active", "is_staff"]

    def create(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.pop('confirm_password')
        user = User(**attrs)
        match(password, confirm_password):
            case(None,_):
                raise serializers.ValidationError({"password": "Password is required."})
            case(_,None):
                raise serializers.ValidationError({"password": "Password confirmation is required."})
            case(_,_) if password != confirm_password:
                raise serializers.ValidationError({"password": "Passwords do not match."})
            case (_,_):
                user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.get('password', None)
        if password:
            instance.set_password(password)
        return super().update(instance, validated_data)

    def delete(self, instance):
        instance.is_active = False
        instance.save()
        return instance

class UserPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
        ]


class UserUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
            "is_active",
            "is_staff",
        ]

    def update(self, instance, validated_data):
        password = validated_data.get('password', None)
        if password:
            instance.set_password(password)
        return super().update(instance, validated_data)
