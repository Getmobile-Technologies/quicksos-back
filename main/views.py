from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .serializers import EscalateSerializer, AgencySerializer, MessageSerializer
from drf_yasg.utils import swagger_auto_schema
from .models import Agency, Message
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsAdmin, IsAdminOrReadOnly, IsAgent, IsAgentOrAdmin, IsEscalator


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
@permission_classes([IsAgentOrAdmin])
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
def peding_message(request):        
    if request.method == "GET":
        messages = Message.objects.filter(is_active=True, status = "pending")
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


@swagger_auto_schema("post", request_body=AgencySerializer())
@api_view(["GET", "POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAdminOrReadOnly])
def agencies(request):
    
    if request.method == "GET":
        agency = Agency.objects.filter(is_active=True)
        serializer = AgencySerializer(agency, many=True)
        data = {"message":"success",
                "data":serializer.data}
        
        return Response(data,status=status.HTTP_200_OK)
    
    elif request.method == "POST":
        serializer = AgencySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            
            return Response({"message":"success"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"error":serializer.errors,"message":"failed"}, status=status.HTTP_400_BAD_REQUEST)
         
    
    
    
@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAdmin])
def agency_detail(request, agency_id):
    try:
        obj = Agency.objects.get(id=agency_id, is_active=True)
    except Message.DoesNotExist:
        errors = {
                "message":"failed",
                "errors": f'Agency with id {agency_id} not found'
                }
        return Response(errors, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer =AgencySerializer(obj)
        data = {
                "message":"success",
                "data":serializer.data
                }
            
        return Response(data, status=status.HTTP_200_OK)
        
    
    elif request.method == 'PUT':
        serializer = AgencySerializer(obj, data=request.data, partial=True)
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
            obj.agencies.set(serializer.validated_data['agencies'])
            obj.status="escalated"
            obj.save()
        
            return Response({"message":"successful"}, status=status.HTTP_204_NO_CONTENT)
        else:
            errors = {
                "message":"failed",
                "errors":serializer.errors
                }
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsEscalator])
def escalated_message(request):        
    if request.method == "GET":
        messages = Message.objects.filter(is_active=True, status="escalated",agencies=request.user.agency )
        serializer = MessageSerializer(messages, many=True)
        data = {"message":"success",
                "data":serializer.data}
        
        return Response(data,status=status.HTTP_200_OK)