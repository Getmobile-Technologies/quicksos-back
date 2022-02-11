from rest_framework import serializers
from .models import WhatsappMessage


class MessageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = WhatsappMessage
        fields = '__all__'