from unittest import case
from rest_framework import serializers

from main.serializers import AgencySerializer, MessageSerializer
from .models import AssignedCase, Report, RequestSupport


class AssignedCaseSerializer(serializers.ModelSerializer):
    case_detail = serializers.ReadOnlyField()
    issue = serializers.ReadOnlyField()
    img_url = serializers.ReadOnlyField()
    report_detail = serializers.ReadOnlyField()
    
    class Meta:
        model = AssignedCase
        fields = '__all__'
        
        
class ReportSerializer(serializers.ModelSerializer):
    img1 = serializers.ImageField()
    img2 = serializers.ImageField(required=False)
    # mark_complete = serializers.BooleanField()
    
    class Meta:
        model=Report
        fields = '__all__'
        
        
        
class RequestSupportSerializer(serializers.ModelSerializer):
    case_detail = MessageSerializer(read_only=True)
    agency_detail = AgencySerializer(read_only=True,many=True)
    sender_detail = serializers.ReadOnlyField()
    
    class Meta:
        model = RequestSupport
        fields = '__all__'
        extra_kwargs = {
    'case': {'write_only': True},
    "agencies": {'write_only': True},
    "sender" : {'write_only': True},
    
}