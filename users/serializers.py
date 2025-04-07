from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email',
                  'first_name', 'last_name', 'depertment']


class UserCreateSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'confirm_password',
                  'first_name', 'last_name', 'depertment']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        # Check if passwords match
        if data['password'] != data.pop('confirm_password'):
            raise serializers.ValidationError(
                {"confirm_password": "Passwords do not match."})
        return data

    def create(self, validated_data):
        # Hash the password before saving
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)


class UserUpdateSerializer(serializers.ModelSerializer):
    current_password = serializers.CharField(write_only=True, required=False)
    new_password = serializers.CharField(write_only=True, required=False)
    confirm_new_password = serializers.CharField(
        write_only=True, required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'current_password', 'new_password',
                  'confirm_new_password', 'first_name', 'last_name', 'depertment']
        extra_kwargs = {
            'username': {'required': False},
            'email': {'required': False},
            'first_name': {'required': False},
            'last_name': {'required': False},
            'depertment': {'required': False}
        }

    def validate(self, data):
        # Check if user is trying to update password
        if 'new_password' in data:
            # Ensure all password fields are provided
            if not all(field in data for field in ['current_password', 'confirm_new_password']):
                raise serializers.ValidationError({
                    "password": "Current password and password confirmation are required."
                })

            # Check if current password is correct
            from django.contrib.auth.hashers import check_password
            if not check_password(data['current_password'], self.instance.password):
                raise serializers.ValidationError(
                    {"current_password": "Current password is incorrect."})

            # Check if new passwords match
            if data['new_password'] != data.pop('confirm_new_password'):
                raise serializers.ValidationError(
                    {"confirm_new_password": "New passwords do not match."})

            # Hash the new password
            data['password'] = make_password(data.pop('new_password'))

        # Remove current_password if present
        if 'current_password' in data:
            data.pop('current_password')

        return data


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
