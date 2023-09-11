from rest_framework import serializers

class PasswordCheckSerializer(serializers.Serializer):
    password = serializers.CharField()
