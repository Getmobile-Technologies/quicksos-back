from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from main.helpers.date_format import get_month

from .serializers import AssignedCaseSerializer, ReportSerializer, RequestSupportSerializer
from drf_yasg.utils import swagger_auto_schema
from .models import AssignedCase, Report, RequestSupport
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsAdmin, IsAgent, IsEscalator, IsResponder
from rest_framework.exceptions import PermissionDenied
import cloudinary
from django.utils import timezone

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
            
            instance = serializer.save()
            instance.escalator = request.user
            instance.save()
            
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
        query = request.GET.get("filterBy")
        
        
        if request.user.role == "escalator":
            obj = AssignedCase.objects.filter(responder__agency=request.user.agency, is_active=True)
        elif request.user.role == "first_responder":
            obj = AssignedCase.objects.filter(responder=request.user, is_active=True).exclude(status="complete")
        else:
            raise PermissionDenied({"error":"You do not have the permission to view this"})
        
        if query == "today":
            date = timezone.now()
            obj = obj.filter(date_created__gte=date)
            
        if query == "recent":
            date = timezone.now() - timezone.timedelta(hours=6)
            obj = obj.filter(date_created__gte=date)
            
        serializer = AssignedCaseSerializer(obj, many=True)
        
        
        data = {
            "message":"success",
            'data' : serializer.data
            }
        
        return Response(data, status=status.HTTP_200_OK)



@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsResponder])
def respond(request, assigned_case_id):
    try:
        obj = AssignedCase.objects.get(id=assigned_case_id, is_active=True)
        
        if obj.responded==False:
            obj.status="responded"
            obj.responded=True
            obj.responded_at = timezone.now()
            obj.save()
            return Response({"message":"successful"}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({"errors":"You have already responded to this case"}, status=status.HTTP_400_BAD_REQUEST)
        
        
    except AssignedCase.DoesNotExist:
        errors = {
                "message":"failed",
                "errors": f'Case not found'
                }
        return Response(errors, status=status.HTTP_404_NOT_FOUND)
    

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsResponder])
def has_arrived(request, assigned_case_id):
    try:
        obj = AssignedCase.objects.get(id=assigned_case_id, is_active=True, responded=True)
        
        if obj.arrived==False:
            obj.status="arrived"
            obj.arrived=True
            obj.arrived_at=timezone.now()
            obj.save()
            return Response({"message":"successful"}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({"errors":"You have arrived at this case before."}, status=status.HTTP_400_BAD_REQUEST)
        
    except AssignedCase.DoesNotExist:
        errors = {
                "message":"failed",
                "errors": f'Case not found or has not been responded to.'
                }
        return Response(errors, status=status.HTTP_404_NOT_FOUND)
    
    
@swagger_auto_schema("post", request_body=ReportSerializer())
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsResponder])
def add_report(request, assigned_case_id):
    try:
        obj = AssignedCase.objects.get(id=assigned_case_id, is_active=True, responded=True, arrived=True)
    except AssignedCase.DoesNotExist:
        errors = {
                "message":"failed",
                "errors": f'Case not found or has not been responded to.'
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
            
           
            obj.status = "complete"
            obj.completed_at = timezone.now()
            obj.save()
            
            if request.user.agency.acronym == "LASEMA": #TODO: add field to distinguish supervising agency in the agency DB
                obj.case.status = "completed"
                obj.case.save()
                
            return Response({"message":"successful"}, status=status.HTTP_202_ACCEPTED)
        else:
            errors = {
                "message":"failed",
                "errors":serializer.errors
                }
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        
        
@swagger_auto_schema("post", request_body=RequestSupportSerializer())
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsResponder])
def request_backup(request):
    if request.method == "POST":
        serializer = RequestSupportSerializer(data=request.data)

        if serializer.is_valid():
    
            
            agencies_ = serializer.validated_data.pop("agencies")
            
            support = RequestSupport.objects.create(**serializer.validated_data)
            support.agencies.set(agencies_)
            support.sender=request.user
            support.save()
            
            return Response({"message":"success"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"error":serializer.errors,"message":"failed"}, status=status.HTTP_400_BAD_REQUEST)
    
    

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAdmin])
def requested_backups(request):
    if request.method == "GET":
        requests = RequestSupport.objects.filter(is_active=True)
        serializer = RequestSupportSerializer(requests, many=True)

        
        return Response({"message":"success", "data":serializer.data}, status=status.HTTP_200_OK)
    
    
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAdmin])
def respond_to_request(request, request_id):
    try:
        obj = RequestSupport.objects.get(id=request_id, is_active=True, status="pending")
        
        
        obj.status="approved"
        obj.save()
        return Response({"message":"successful"}, status=status.HTTP_202_ACCEPTED)
        
    except RequestSupport.DoesNotExist:
        errors = {
                "message":"failed",
                "errors": f'Backup request not found'
                }
        return Response(errors, status=status.HTTP_404_NOT_FOUND)
        
# <User: desmond@gmail.com>, <User: admin@example.com>, <User: admin2@example.com>, <User: response@example.com>, <User: agent@example.com>]
# password: qwertyuiop




        

        