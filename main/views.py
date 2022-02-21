from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .serializers import MessageSerializer
from drf_yasg.utils import swagger_auto_schema
from .models import WhatsappMessage
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsAdmin


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
@permission_classes([IsAuthenticated])
def get_report(request):        
    if request.method == "GET":
        messages = WhatsappMessage.objects.filter(is_active=True)
        serializer = MessageSerializer(messages, many=True)
        data = {"message":"success",
                "data":serializer.data}
        
        return Response(data,status=status.HTTP_200_OK)
    
    
@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def report_detail(request, report_id):
    try:
        obj = WhatsappMessage.objects.get(id=report_id, is_active=True)
    except WhatsappMessage.DoesNotExist:
        errors = {
                "message":"failed",
                "errors": f'Report with id {report_id} not found'
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
    