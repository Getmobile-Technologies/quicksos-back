from rest_framework import serializers
from .models import Escalator, Message


class MessageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Message
        fields = '__all__'
        
        
class EscalatorSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Escalator
        fields = '__all__'
        
        
class EscalateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Message
        fields = ['escalators']