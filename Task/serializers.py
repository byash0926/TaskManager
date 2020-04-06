from rest_framework import serializers
from .models import Task
from django.contrib.auth.models import User



class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'name', 'description', 'super_task', 'user')


class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style = {'inpute_type':'password'}, write_only = True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')
        extra_kwargs = {
            'password' : {'write_only' : True}
        }

    def save(self):
        user = User(
            username = self.validated_data['username'],
            email = self.validated_data['email']
        )

        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.validationError({'password' : 'password must match'})
        user.set_password(password)
        user.save()
        return user