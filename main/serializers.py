from rest_framework import serializers
from .models import Agency, Answer, Issue, Message, Question
from rest_framework.exceptions import ValidationError
from django.utils import timezone

class PostAnswerSerializer(serializers.Serializer):
    question = serializers.UUIDField()
    answer = serializers.CharField(max_length=5000)
    
    
    def validate_question(self, value):
        try:
            value = Question.objects.get(id=value, is_active=True)
            
        except Question.DoesNotExist:
            raise ValidationError(detail="Question Id does not exist")
        
        return value
            
class MessageSerializer(serializers.ModelSerializer):
    responses = PostAnswerSerializer(many=True, write_only=True)
    response_data = serializers.ReadOnlyField()
    issue = serializers.ReadOnlyField()
    agency_detail = serializers.ReadOnlyField()    
    class Meta:
        model = Message
        fields = '__all__'
        
    def create(self, validated_data):
        responses = validated_data.pop("responses")
        agencies = validated_data.pop("agencies", None)
        message = Message.objects.create(**validated_data)

        if agencies:
            message.agencies.set(agencies)
            message.status = "escalated"
            message.date_escalated = timezone.now()
            message.save()
            
        ans = [Answer(**response, message=message) for response in responses]
        Answer.objects.bulk_create(ans)   
        return message

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'
        
class IssueSerializer(serializers.ModelSerializer):
    question_list = serializers.ReadOnlyField()
    questions= QuestionSerializer(many=True, write_only=True)
    class Meta:
        model = Issue
        fields = '__all__'
        
        
    def create(self, validated_data):
        questions = validated_data.pop("questions")
        
        issue = Issue.objects.create(**validated_data)
        quests = []
        for question in questions:
            question["issue"] = issue
            quests.append(Question(**question))
        Question.objects.bulk_create(quests)    
        return issue
               
    # TODO:Implement solution to order questions
               
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
        error = False
        if  attrs.get('agent_note') is None or len(attrs.get('agent_note')) <= 0:
            err['agencies'] = "Please add agencies you want to escalate to."
            error = True
        if attrs.get('agent_note') == "" or attrs.get('agent_note')  is None:
            err["agent_note"] = "Please add note for escalators"
            error = True
        
        if error == True:
            
            raise ValidationError(err)
        else:
            return attrs