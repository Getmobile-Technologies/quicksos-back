from rest_framework import serializers
from .models import Agency, Answer, EmergencyCode, Issue, Message, Question
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
        emergency_code = validated_data.pop("emergency_code", None)
        
        message = Message.objects.create(**validated_data)
        
        if "issues" in validated_data.keys():
            incident = validated_data.pop("issues")
            message.incident = incident
            
        ### create a question-answer object for the reported case
        ans = []
        for response in responses: 
            question_obj = response.pop('question')
            question = question_obj.question 
             
            answer = Answer(**response, message=message, question=question)
            ans.append(answer) 
        else:
            Answer.objects.bulk_create(ans)   
            
        
        
        #escalaste the case if there an emergence code was issued
        if emergency_code:
            message.status = "escalated"
            message.date_escalated = timezone.now()
            message.emergency_code = emergency_code
            
        message.save()
        
        return message

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'
        
class IssueSerializer(serializers.ModelSerializer):
    question_list = serializers.ReadOnlyField()
    questions= QuestionSerializer(many=True, write_only=True)
    case_count = serializers.ReadOnlyField()
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
        fields = ['emergency_code', 'agent_note', "category"]
        
        
    def validate(self, attrs):
        err = {}
        error = False
        if  attrs.get('emergency_code') is None:
            err['emergency_code'] = "Please select an emergency code for this case."
            error = True
        if attrs.get('agent_note') == "" or attrs.get('agent_note')  is None:
            err["agent_note"] = "Please add note for escalators"
            error = True
            
        # if attrs.get('local_gov') == "" or attrs.get('local_gov')  is None:
        #     err["local_gov"] = "Please select the appropriate local government for this case."
        #     error = True
            
        if attrs.get('category') == "" or attrs.get('category')  is None:
            err['category'] = "Please select a category for this case"
            error = True
        
            
        if error == True:
            
            raise ValidationError(err)
        else:
            return attrs
        

class ArchiveSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Message
        fields = ['archive_reason', "category"]
        
        
    def validate(self, attrs):
        err = {}
        error = False
        if  attrs.get('archive_reason') is None:
            err['archive_reason'] = "Please state reason for archive"
            error = True
       
            
        if attrs.get('category') == "" or attrs.get('category')  is None:
            err['category'] = "Please select a category for this case"
            error = True
        
            
        if error == True:
            
            raise ValidationError(err)
        else:
            return attrs
        
        
class EmergencyCodeSerializer(serializers.ModelSerializer):
    agencies = serializers.ReadOnlyField()
    
    class Meta:
        model = EmergencyCode
        fields = '__all__'
        
        extra_kwargs = {'agency': {'write_only': True}}
        
        
    # def get_agencies(self, agencies):
    #     package_ids = []
    #     for package in a:
    #         package_instance, created = Package.objects.get_or_create(pk=package.get('id'), defaults=package)
    #         package_ids.append(package_instance.pk)
    #     return package_ids

    # def create_or_update_packages(self, packages):
    #     package_ids = []
    #     for package in packages:
    #         package_instance, created = Package.objects.update_or_create(pk=package.get('id'), defaults=package)
    #         package_ids.append(package_instance.pk)
    #     return package_ids

    def create(self, validated_data):
        agencies = validated_data.pop('agency')
        emergency_code = EmergencyCode.objects.create(**validated_data)
        emergency_code.agency.set(agencies)
        return emergency_code

    def update(self, instance, validated_data):
        
        if "agency" in validated_data.keys():
            
            agencies = validated_data.pop('agency')
            
            instance.agency.set(agencies)
            
        fields = validated_data.keys()
        for field in fields:
            try:
                setattr(instance, field, validated_data[field])
            except KeyError:  # validated_data may not contain all fields during HTTP PATCH
                pass
            
        instance.save()
        return instance