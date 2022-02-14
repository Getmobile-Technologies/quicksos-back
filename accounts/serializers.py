from rest_framework import serializers
from django.contrib.auth import get_user_model
 
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=300, required=False,allow_blank=True)
    class Meta():
        model = User
        fields = '__all__'
        
