from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .serializers import EscalateSerializer, EscalatorSerializer, MessageSerializer
from drf_yasg.utils import swagger_auto_schema
from .models import Escalator, Message
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsAdmin, IsAdminOrReadOnly, IsAgent, IsEscalator


@swagger_auto_schema("post", request_body=MessageSerializer())
@api_view(["POST"])
def add_message(request):
    
    if request.method == "POST":
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            
            return Response({"message":"success"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"error":serializer.errors,"message":"failed"}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAgent])
def get_message(request):        
    if request.method == "GET":
        messages = Message.objects.filter(is_active=True)
        serializer = MessageSerializer(messages, many=True)
        data = {"message":"success",
                "data":serializer.data}
        
        return Response(data,status=status.HTTP_200_OK)
    
    
@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAgent])
def message_detail(request, message_id):
    try:
        obj = Message.objects.get(id=message_id, is_active=True)
    except Message.DoesNotExist:
        errors = {
                "message":"failed",
                "errors": f'Message with id {message_id} not found'
                }
        return Response(errors, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer =MessageSerializer(obj)
        data = {
                "message":"success",
                "data":serializer.data
                }
            
        return Response(data, status=status.HTTP_200_OK)
        
    
    elif request.method == 'PUT':
        serializer = MessageSerializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            data = {
                "message":"success",
                "data":serializer.data
                }
            
            return Response(data, status=status.HTTP_202_ACCEPTED)
        else:
            errors = {
                "message":"failed",
                "errors":serializer.errors
                }
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        
    elif request.method == 'DELETE':
        obj.delete()
        data = {
                "message":"success"
                }
            
        return Response(data, status=status.HTTP_204_NO_CONTENT)


@swagger_auto_schema("post", request_body=EscalatorSerializer())
@api_view(["GET", "POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAdminOrReadOnly])
def escalators(request):
    
    if request.method == "GET":
        escalators = Escalator.objects.filter(is_active=True)
        serializer = EscalatorSerializer(escalators, many=True)
        data = {"message":"success",
                "data":serializer.data}
        
        return Response(data,status=status.HTTP_200_OK)
    
    elif request.method == "POST":
        serializer = EscalatorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            
            return Response({"message":"success"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"error":serializer.errors,"message":"failed"}, status=status.HTTP_400_BAD_REQUEST)
         
    
    
    
@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAdmin])
def escalator_detail(request, escalator_id):
    try:
        obj = Escalator.objects.get(id=escalator_id, is_active=True)
    except Message.DoesNotExist:
        errors = {
                "message":"failed",
                "errors": f'Escalator with id {escalator_id} not found'
                }
        return Response(errors, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer =EscalatorSerializer(obj)
        data = {
                "message":"success",
                "data":serializer.data
                }
            
        return Response(data, status=status.HTTP_200_OK)
        
    
    elif request.method == 'PUT':
        serializer = EscalatorSerializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            data = {
                "message":"success",
                "data":serializer.data
                }
            
            return Response(data, status=status.HTTP_202_ACCEPTED)
        else:
            errors = {
                "message":"failed",
                "errors":serializer.errors
                }
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        
    elif request.method == 'DELETE':
        obj.delete()
        data = {
                "message":"success"
                }
            
        return Response(data, status=status.HTTP_204_NO_CONTENT)
    


@swagger_auto_schema("post", request_body=EscalateSerializer())
@authentication_classes([JWTAuthentication])
@permission_classes([IsAgent])
@api_view(['POST'])
def escalate(request, message_id):
    try:
        obj = Message.objects.get(id=message_id, is_active=True, status="pending")
        
    except Message.DoesNotExist:
        errors = {
                "message":"failed",
                "errors": f'Message with id {message_id} not found or has been escalated'
                }
        return Response(errors, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "POST":
        
        serializer = EscalateSerializer(data=request.data)
        
        if serializer.is_valid():
            obj.escalators.set(serializer.validated_data['escalators'])
            obj.status="escalated"
            obj.save()
        
        return Response({"message":"successful"}, status=status.HTTP_204_NO_CONTENT)
    

@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsEscalator])
def escalated_message(request):        
    if request.method == "GET":
        messages = Message.objects.filter(is_active=True, status="escalated",escalators=request.user.escalator )
        serializer = MessageSerializer(messages, many=True)
        data = {"message":"success",
                "data":serializer.data}
        
        return Response(data,status=status.HTTP_200_OK)