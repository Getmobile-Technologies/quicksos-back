from rest_framework import serializers
from .models import Agency, Message


class MessageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Message
        fields = '__all__'
        
        
class AgencySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Agency
        fields = '__all__'
        
        
class EscalateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Message
        fields = ['agencies']