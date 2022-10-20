from django.forms import model_to_dict
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .serializers import ArchiveSerializer, EmergencyCodeSerializer, EscalateSerializer, AgencySerializer, IssueSerializer, MessageSerializer, QuestionSerializer
from drf_yasg.utils import swagger_auto_schema
from .models import Agency, EmergencyCode, Issue, Message, Question, User
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsAdmin, IsAdminOrReadOnly, IsAgent, IsAgentOrAdmin, IsEscalator
from django.utils import timezone
from rest_framework.authentication import TokenAuthentication
from .helpers.check_agency import validate_responders


@swagger_auto_schema("post", request_body=MessageSerializer())
@api_view(["POST"])
@authentication_classes([JWTAuthentication, TokenAuthentication])
@permission_classes([IsAgentOrAdmin])
def add_message(request):
    
    if request.method == "POST":
        serializer = MessageSerializer(data=request.data)

        if serializer.is_valid():
    
            if serializer.validated_data.get("provider") == "call":
                emergency_code = serializer.validated_data.get('emergency_code')
                if validate_responders(emergency_code.agency.all()):
                    serializer.save()
            else:
    
                serializer.save()
            
            
            
            return Response({"message":"success"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"error":serializer.errors,"message":"failed"}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAgentOrAdmin])
def get_message(request):        
    if request.method == "GET":
        
        date = request.GET.get("filterDate")
        
        messages = Message.objects.filter(is_active=True)
        
        if date:
            messages = messages.filter(date_created__date=date)
            
        serializer = MessageSerializer(messages, many=True)
        data = {"message":"success",
                "data":serializer.data}
        
        return Response(data,status=status.HTTP_200_OK)
    
    
@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAgent])
def pending_message(request):        
    if request.method == "GET":
        date = request.GET.get("filterDate")
        
        messages = Message.objects.filter(is_active=True, status = "pending")
        
        
        
        if date:
            messages = messages.filter(date_created__date=date)
            
        serializer = MessageSerializer(messages, many=True)
        data = {"message":"success",
                "data":serializer.data}
        
        return Response(data,status=status.HTTP_200_OK)
    
    
@api_view(["GET", "PUT", "DELETE"])
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
         
    
    
    
@api_view(["GET", "PUT", "DELETE"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAdmin])
def agency_detail(request, agency_id):
    try:
        obj = Agency.objects.get(id=agency_id, is_active=True)
    except Agency.DoesNotExist:
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
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAgent])
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
            emergency_code = serializer.validated_data.get('emergency_code')
            
            #check all the agencies to be escalated to, if any does not have an escalator, raise an error.
            if validate_responders(emergency_code.agency.all()):
                    
                # print(request.user)
                obj.agent = request.user
                obj.emergency_code = emergency_code
                obj.status= "escalated"
                obj.date_escalated = timezone.now()
                # obj.local_gov = serializer.validated_data.get('local_gov')
                obj.agent_note = serializer.validated_data.get('agent_note')
                
                obj.category = serializer.validated_data.get('category')
                
                obj.save()
            
                return Response({"message":"successful"}, status=status.HTTP_201_CREATED)
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
        date = request.GET.get("filterDate")
                
        messages = Message.objects.filter(is_active=True, status="escalated",emergency_code__agency=request.user.agency )
        
        if date:
            messages = messages.filter(date_escalated__date=date)
            
        serializer = MessageSerializer(messages, many=True)
        data = {"message":"success",
                "data":serializer.data}
        
        return Response(data,status=status.HTTP_200_OK)
    
    

@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def message_report(request, message_id):        
    if request.method == "GET":
        try:
            message = Message.objects.get(is_active=True, id=message_id)
            msg_serializer = MessageSerializer(message)
            data_ = {"message_data":msg_serializer.data,
                "responder_reports":[{
                    "first_responder": model_to_dict(case.responder,exclude=
                                                 ['password',
                                                  'groups',
                                                  'user_permissions',
                                                  'agency',
                                                  'last_login']),
                    "agency":model_to_dict(case.responder.agency),
                    "escalator_note": case.escalator_note, 
                    "responder_status":case.status, 
                    'reports':case.report_detail,
                    "assigned_date" : case.date_created,
                    } for case in message.assigned.all()],
                     }
            
            data = {"message":"success",
                    "data":data_}
            
            return Response(data,status=status.HTTP_200_OK)
        except Message.DoesNotExist:
            errors = {
                    "message":"failed",
                    "errors": f'Message not found'
                    }
            return Response(errors, status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAgent])
def mark_as_emergency(request, message_id):        
    if request.method == "GET":
        try:
            message = Message.objects.get(is_active=True, id=message_id)
            message.is_emergency=True
            message.save()
            
            data = {"message":"success"
                    }
            
            return Response(data,status=status.HTTP_200_OK)
        except Message.DoesNotExist:
            errors = {
                    "message":"failed",
                    "errors": f'Message not found'
                    }
            return Response(errors, status=status.HTTP_404_NOT_FOUND)
        
        
        
        
# =========== CRUD QUESTIONS, ISSUES AND RESPONSES ================
@swagger_auto_schema("post", request_body=IssueSerializer())
@api_view(["GET", "POST"])
@authentication_classes([JWTAuthentication, TokenAuthentication])
@permission_classes([IsAdminOrReadOnly])
def issues(request):
    
    if request.method == "GET":
        issue = sorted(Issue.objects.filter(is_active=True), key=lambda t: t.case_count, reverse=True)
        
        serializer = IssueSerializer(issue, many=True)
        data = {"message":"success",
                "data":serializer.data}
        
        return Response(data,status=status.HTTP_200_OK)
    
    elif request.method == "POST":
        serializer = IssueSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            
            return Response({"message":"success"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"error":serializer.errors,"message":"failed"}, status=status.HTTP_400_BAD_REQUEST)
         
    
    
@swagger_auto_schema(methods=["put","delete"], request_body=IssueSerializer())
@api_view(["GET", "PUT", "DELETE"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAdmin])
def issue_detail(request, issue_id):
    try:
        obj = Issue.objects.get(id=issue_id, is_active=True)
    except Issue.DoesNotExist:
        errors = {
                "message":"failed",
                "errors": f'Issue with id {issue_id} not found'
                }
        return Response(errors, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer =IssueSerializer(obj)
        data = {
                "message":"success",
                "data":serializer.data
                }
            
        return Response(data, status=status.HTTP_200_OK)
        
    
    elif request.method == 'PUT':
        serializer = IssueSerializer(obj, data=request.data, partial=True)
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
    
    
@swagger_auto_schema(methods=["post"], request_body=QuestionSerializer())
@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAdmin])
def add_new_questions(request, issue_id):  
    try:
        obj = Issue.objects.get(id=issue_id, is_active=True)
    except Issue.DoesNotExist:
        errors = {
                "message":"failed",
                "errors": f'Issue with id {issue_id} not found'
                }
        return Response(errors, status=status.HTTP_404_NOT_FOUND)
    
    
    if request.method == "POST":
        serializer = QuestionSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            
            return Response({"message":"success"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"error":serializer.errors,"message":"failed"}, status=status.HTTP_400_BAD_REQUEST)
     
    
    
    
@swagger_auto_schema(methods=["put","delete"], request_body=IssueSerializer())
@api_view(['PUT',"DELETE"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAdmin])
def question_detail(request, question_id):
    try:
        obj = Question.objects.get(id=question_id, is_active=True)
    except Question.DoesNotExist:
        errors = {
                "message":"failed",
                "errors": f'Question with id {question_id} not found'
                }
        return Response(errors, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer =QuestionSerializer(obj)
        data = {
                "message":"success",
                "data":serializer.data
                }
            
        return Response(data, status=status.HTTP_200_OK)
        
    
    elif request.method == 'PUT':
        serializer = QuestionSerializer(obj, data=request.data, partial=True)
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
    
    
@api_view(["GET"])
@authentication_classes([JWTAuthentication, TokenAuthentication])
@permission_classes([IsAdminOrReadOnly])
def escalated_cases_by_agency(request):
    """Provides analytics for cases escalated to agencies. Allows parameters to filter by local_gov, month and year."""
    
    #get escalated cases by agencies    
    
    local_gov = request.GET.get("local_gov")
    month = request.GET.get("month")
    year = request.GET.get("year")
    start_date = request.GET.get("startDate")
    end_date = request.GET.get("endDate")

    
    agencies = Agency.objects.filter(is_active=True)
        
    if month or year or start_date or end_date:
        messages = Message.objects.filter(is_active=True)
    else:
        today = timezone.now().date()
        messages = Message.objects.filter(is_active=True, date_escalated__date = today)
        
    
    if local_gov:
        messages = messages.filter(local_gov=local_gov)
        
    if month:
        messages = messages.filter(date_escalated__month=month)
    
    if year:
        messages = messages.filter(date_escalated__year=year)
        
    if start_date:
        messages = messages.filter(date_created__date__gte=start_date)
    
    if end_date:
        messages = messages.filter(date_created__date__lte=end_date)
        
    
    escalation_by_agencies = {agency.acronym: messages.filter(emergency_code__agency=agency).count() for agency in agencies if messages.filter(emergency_code__agency=agency).count() > 0 }
    
    
    data = {
        "message":"success",
        "escalation_by_agencies": escalation_by_agencies
    }
            
    return Response(data, status=status.HTTP_200_OK)


@api_view(["GET"])
@authentication_classes([JWTAuthentication, TokenAuthentication])
@permission_classes([IsAdminOrReadOnly])
def reported_cases_by_issues(request):
    """Provides analytics for cases reported. Allows parameters to filter by local_gov, month and year."""
    
    #get escalated cases by agencies
    
    local_gov = request.GET.get("local_gov")
    month = request.GET.get("month")
    year = request.GET.get("year")
    
    start_date = request.GET.get("startDate")
    end_date = request.GET.get("endDate")

    
    issues = Issue.objects.filter(is_active=True)
    
    if month or year or start_date or end_date:
        messages = Message.objects.filter(is_active=True)
    else:
        today = timezone.now().date()
        messages = Message.objects.filter(is_active=True, date_created__date = today)
    
    if local_gov:
        messages = messages.filter(local_gov=local_gov)
        
    if month:
        messages = messages.filter(date_created__month=month)
    
    if year:
        messages = messages.filter(date_created__year=year)
        
    if start_date:
        messages = messages.filter(date_created__date__gte=start_date)
    
    if end_date:
        messages = messages.filter(date_created__date__lte=end_date)
        
    
    
    report = {}
    # messages = list(filter(lambda x: x.answers.first() is not None, messages))
    for issue in issues:
        
        # total = len(list(filter(lambda message : message.answers.first().question.issue == issue, messages)))
        
        total = messages.filter(incident=issue).count()
        if total > 0:
            report[issue.name] = total
        

    data = {
        "message":"success",
        "report_by_cases": report,
    }
            
    return Response(data, status=status.HTTP_200_OK)
    
    

@api_view(["GET"])
@authentication_classes([JWTAuthentication, TokenAuthentication])
@permission_classes([IsAdminOrReadOnly])
def dashboard(request):
    """Provides analytics for cases reported today"""
    
    #get escalated cases by agencies
    
   
    today = timezone.now().date()
    messages = Message.objects.filter(is_active=True, date_created__date = today)
    
        
    
    
   

    data = {
        "message":"success",
        "reported_cases": messages.count(),
        "pending" : messages.filter(status="pending").count(),
        "escalated" : messages.filter(status="escalated").count(),
        "completed" : messages.filter(status="completed").count(),
        
    }
            
    return Response(data, status=status.HTTP_200_OK)

    
    

@swagger_auto_schema("post", request_body=EmergencyCodeSerializer())
@api_view(["GET", "POST"])
@authentication_classes([JWTAuthentication, TokenAuthentication])
@permission_classes([IsAdminOrReadOnly])
def emergency_codes(request):
    
    if request.method == "GET":
        codes = EmergencyCode.objects.filter(is_active=True)
        
        serializer = EmergencyCodeSerializer(codes, many=True)
        data = {"message":"success",
                "data":serializer.data}
        
        return Response(data,status=status.HTTP_200_OK)
    
    elif request.method == "POST":
        serializer = EmergencyCodeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            
            return Response({"message":"success"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"error":serializer.errors,"message":"failed"}, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(methods=["put","delete"], request_body=EmergencyCodeSerializer())
@api_view(["GET", "PUT", "DELETE"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAdmin])
def emergency_code_detail(request, code_id):
    try:
        obj = EmergencyCode.objects.get(id=code_id, is_active=True)
    except EmergencyCode.DoesNotExist:
        errors = {
                "message":"failed",
                "errors": f'Emergency code with id {code_id} not found'
                }
        return Response(errors, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer =EmergencyCodeSerializer(obj)
        data = {
                "message":"success",
                "data":serializer.data
                }
            
        return Response(data, status=status.HTTP_200_OK)
        
    
    elif request.method == 'PUT':
        serializer = EmergencyCodeSerializer(obj, data=request.data, partial=True)
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
          
        
        
@swagger_auto_schema("post", request_body=ArchiveSerializer())
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAgent])
def archive_case(request, message_id):
    
    """Api view to archive a case that has been reported multiple times"""
    
    try:
        obj = Message.objects.get(id=message_id, is_active=True, status="pending")
    
        
    except Message.DoesNotExist:
        errors = {
                "message":"failed",
                "errors": f'Message with id {message_id} not found'
                }
        return Response(errors, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "POST":
        
        serializer = ArchiveSerializer(data=request.data)
        
        if serializer.is_valid():
            
            request.user = User.objects.first()
            # print(request.user)
            obj.agent = request.user
            obj.status= "archived"
            obj.date_archived = timezone.now()
            obj.archive_reason = serializer.validated_data.get('archive_reason')
            
            obj.category = serializer.validated_data.get('category')
            
            obj.save()
        
            return Response({"message":"successful"}, status=status.HTTP_201_CREATED)
        else:
            errors = {
                "message":"failed",
                "errors":serializer.errors
                }
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        
        
        
