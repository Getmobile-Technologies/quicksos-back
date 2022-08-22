from rest_framework import serializers
from django.contrib.auth import get_user_model
 
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=300, required=False,allow_blank=True, write_only=True)
    image = serializers.ImageField( required=False)
    agency_detail = serializers.ReadOnlyField()
    
    class Meta():
        model = User
        fields = '__all__'
        

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=300)
    firebase_key = serializers.CharField(max_length=1000, allow_blank=True)
    
    
class ChangePasswordSerializer(serializers.Serializer):
    old_password  = serializers.CharField(max_length=200)
    new_password  = serializers.CharField(max_length=200)
    confirm_password  = serializers.CharField(max_length=200)
    
    
    def check_pass(self):
        """ checks if both passwords are the same """
        if self.validated_data['new_password'] != self.validated_data['confirm_password']:
            raise serializers.ValidationError({"error":"Please enter matching passwords"})
        return True

class ChangeFirebaseKey(serializers.Serializer):
    firebase_key = serializers.CharField(max_length=1000, allow_blank=True)
    

    
# class AddFirstResponder