from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .serializers import AssignedCaseSerializer, ReportSerializer
from drf_yasg.utils import swagger_auto_schema
from .models import AssignedCase, Report
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsAdmin, IsAgent, IsEscalator, IsResponder
from rest_framework.exceptions import PermissionDenied
import cloudinary

@swagger_auto_schema("post", request_body=AssignedCaseSerializer())
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsEscalator])
def assign(request):
    if request.method=="POST":
        serializer = AssignedCaseSerializer(data=request.data)
        
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
        



@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def assigned_cases(request):
    if request.method=="GET":
        
        if request.user.role == "escalator":
            obj = AssignedCase.objects.filter(responder__agency=request.user.agency, is_active=True)
        elif request.user.role == "first_responder":
            obj = AssignedCase.objects.filter(responder=request.user, is_active=True) 
        else:
            raise PermissionDenied({"error":"You do not have the permission to view this"})
        
        serializer = AssignedCaseSerializer(obj, many=True)
        
        
        data = {
            "message":"success",
            'data' : serializer.data
            }
        
        return Response(data, status=status.HTTP_200_OK)



@swagger_auto_schema("post", request_body=ReportSerializer())
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsResponder])
def add_report(request, assigned_case_id):
    try:
        obj = AssignedCase.objects.get(id=assigned_case_id, is_active=True, status='pending')
    except AssignedCase.DoesNotExist:
        errors = {
                "message":"failed",
                "errors": f'Case not found or has been completed.'
                }
        return Response(errors, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "POST":
        
        serializer = ReportSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.validated_data['assigned_case'] = obj
            if 'img1' in serializer.validated_data.keys():
                try:
                    image = serializer.validated_data.pop('img1') #get the image file from the request 
                    img = cloudinary.uploader.upload(image, folder = 'quicksos-report-img/') #upload the image to cloudinary
                    serializer.validated_data['image_url1'] = img['secure_url'] #save the image url 
                    
                except Exception:
                    data = {
                        
                        'error' : "Unable to upload picture"
                    }

                    return Response(data, status = status.HTTP_400_BAD_REQUEST)
                
            if 'img2' in serializer.validated_data.keys():
                try:
                    image = serializer.validated_data.pop('img2') #get the image file from the request 
                    img = cloudinary.uploader.upload(image, folder = 'quicksos-report-img/') #upload the image to cloudinary
                    serializer.validated_data['image_url2'] = img['secure_url'] #save the image url 
                
                except Exception:
                    data = {
                        
                        'error' : "Unable to upload picture"
                    }

                    return Response(data, status = status.HTTP_400_BAD_REQUEST)
            serializer.save()
            
            if serializer.validated_data.get('mark_complete') == True:
                obj.status = "complete"
                obj.save()
                
            return Response({"message":"successful"}, status=status.HTTP_202_ACCEPTED)
        else:
            errors = {
                "message":"failed",
                "errors":serializer.errors
                }
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)


# <User: desmond@gmail.com>, <User: admin@example.com>, <User: admin2@example.com>, <User: response@example.com>, <User: agent@example.com>]
# password: qwertyuiop