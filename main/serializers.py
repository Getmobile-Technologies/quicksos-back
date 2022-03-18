from rest_framework import serializers
from .models import Agency, Message
from rest_framework.exceptions import ValidationError


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
        fields = ['agencies', 'agent_note']
        
        
    def validate(self, attrs):
        err = {}
        if  attrs.get('agent_note') is None or len(attrs.get('agent_note')) <= 0:
            err['agencies'] = "Please add agencies you want to escalate to."
        if attrs.get('agent_note') == "" or attrs.get('agent_note')  is None:
            err["agent_note"] = "Please add note for escalators"
        
        raise ValidationError(err)