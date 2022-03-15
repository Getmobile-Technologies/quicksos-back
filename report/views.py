from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .serializers import ReportSerializer
from drf_yasg.utils import swagger_auto_schema
from .models import Report
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsAdmin, IsAgent, IsEscalator


@swagger_auto_schema("post", request_body=ReportSerializer())
@authentication_classes([JWTAuthentication])
@permission_classes([IsEscalator])
@api_view(['POST'])
def assign(request):
    if request.method=="POST":
        serializer = ReportSerializer(data=request.data)
        
        if serializer.is_valid():
            message = serializer.validated_data['case']
            message.status = "assigned"
            message.save()
            
            serializer.save()
            
            data = {
                "message":"success"
                }
            
            return Response(data, status=status.HTTP_202_ACCEPTED)
        else:
            errors = {
                "message":"failed",
                "errors":serializer.errors
                }
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        

