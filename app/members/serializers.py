from rest_framework import serializers
from rest_framework.authtoken.models import Token

from members.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','email', 'username', 'password']

    def save(self, **kwargs):
        username = self.validated_data['username']
        password = self.validated_data['password']
        email = self.validated_data['email']
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email
        )
        return user